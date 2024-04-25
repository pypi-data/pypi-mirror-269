###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from typing import Any
from uuid import uuid4
from google.cloud import firestore
from google.cloud.firestore import CollectionReference, Query
from google.cloud.firestore_v1.base_client import DEFAULT_DATABASE as _DEFAULT_DATABASE
from everysk.config import settings
from everysk.core.compress import compress_pickle, decompress_pickle
from everysk.core.datetime import Date, DateTime
from everysk.core.fields import DateTimeField, ListField, StrField
from everysk.core.redis import RedisCacheCompressed, RedisLock
from everysk.core.object import BaseDict, BaseObject


class FirestoreClient(BaseObject):
    """
    Client that creates a connection with the Firestore database.
    If the project name and the database name are not passed as params we use
    the ones that are on the settings module.

    Example:

        >>> from everysk.core.firestore import FirestoreClient
        >>> FirestoreClient(project_name='teste', database_name='default')

    """
    ## Private attributes
    # Here we really need the global behavior
    _connections: dict = {}

    ## Public attributes
    database_name = StrField()
    project_name = StrField()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if self.database_name is None:
            self.database_name = _DEFAULT_DATABASE

        if self.project_name is None:
            self.project_name = settings.EVERYSK_GOOGLE_CLOUD_PROJECT

    @property
    def connection(self):
        """
        This property returns the correct connection to access Firestore.
        If the connection is already created we just return it otherwise we need to create.
        We use lock to avoid concurrency on connection creation.
        """
        key = f'{self.project_name}-{self.database_name}'
        try:
            # First we ty to get the connection
            return FirestoreClient._connections[key]
        except KeyError:
            # If the connection does not exist we create it
            # The lock is to avoid creating multiple connections, because this is expensive
            lock = RedisLock(name=f'everysk-lib-firestore-lock-connection-{key}', timeout=600)
            lock.acquire(blocking=True)
            # At this moment we have 2 facts:
            # 1 - We are the first to get the lock or;
            # 2 - Some other process released the lock and we get it;
            # On the first case we need to get the real connection.
            # On the second case we already have the connection created.
            # so we check just to be fast.
            try:
                if key not in FirestoreClient._connections:
                    FirestoreClient._connections[key] = firestore.Client(project=self.project_name, database=self.database_name)
            finally:
                # We need to always release the lock
                lock.release()

        return FirestoreClient._connections[key]

    def get_collection(self, collection_name: str) -> CollectionReference:
        """
        Returns the CollectionReference object that refers to the collection_name inside Firestore.

        Args:
            collection_name (str): The name of the collection.
        """
        return self.connection.collection(collection_name)


class BaseDocumentConfig(BaseObject):
    """
    Base class that has all config values used inside the Document class.
    """
    ## Private attributes
    _client: FirestoreClient = None

    ## Public attributes
    collection_name = StrField()
    database_name = StrField()
    excluded_keys = ListField()
    project_name = StrField()

    @property
    def client(self) -> FirestoreClient:
        """
        We use this property to create the connection if it does not exists.
        """
        if self._client is None:
            self._client = FirestoreClient(project_name=self.project_name, database_name=self.database_name)
        return self._client

    @property
    def collection(self) -> CollectionReference:
        """ Alias to the CollectionReference on Firestore"""
        if not self.collection_name:
            raise AttributeError('The collection_name is empty.')

        return self.client.get_collection(self.collection_name)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Fix to keep the excluded_keys attribute always a list
        if self.excluded_keys is None:
            self.excluded_keys = []


class Document(BaseDict):
    """
    Class that represents a Document in Firestore database.
    All documents that use this class will have these fields:

    - created_at: A DateTime field that is filled when we create the object.
    - firestore_id: A string field that has the Document ID from Firestore.
    - updated_at: A DateTime field that is filled when we save the object.
    """
    # This need to be configured on child classes
    class Config(BaseDocumentConfig):
        pass

    ## Public attributes
    config: BaseDocumentConfig = None # We put this here to use the Autocomplete correctly
    created_at = DateTimeField()
    firestore_id = StrField()
    updated_at = DateTimeField()

    ## Private methods
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            kwargs[key] = self._parser_in(value)

        super().__init__(**kwargs)
        if self.created_at is None:
            self.created_at = DateTime.now()

    def _parser_in(self, obj: Any) -> Any:
        """ Parse all data to convert in python format to be used on the instance. """
        ret = obj
        if isinstance(obj, dict):
            ret = {}
            for key, value in obj.items():
                ret[key] = self._parser_in(value)

        elif isinstance(obj, list):
            ret = []
            for item in obj:
                ret.append(self._parser_in(item))

        elif isinstance(obj, str):
            try:
                ret = Date.fromisoformat(obj)
            except (TypeError, ValueError):
                try:
                    ret = DateTime.fromisoformat(obj)
                except (TypeError, ValueError):
                    pass

        elif isinstance(obj, bytes):
            try:
                ret = decompress_pickle(obj)
            except Exception: # pylint: disable=broad-except
                pass

        return ret

    def _parser_out(self, obj: Any) -> Any:
        """ Parse all data to convert in Firestore format to be used on the save to Firestore. """
        ret = obj
        if obj is not None:
            if isinstance(obj, dict):
                ret = {}
                for key, value in obj.items():
                    ret[key] = self._parser_out(value)

            elif isinstance(obj, list):
                ret = []
                for item in obj:
                    ret.append(self._parser_out(item))

            elif hasattr(obj, 'isoformat'):
                ret = obj.isoformat()

            # All other attributes will be treated as obj and sent to Firestore as byte.
            elif not isinstance(obj, (bytes, bool, float, int, str)):
                ret = compress_pickle(obj)

        return ret

    ## Public methods
    @classmethod
    def loads(cls, field: str, condition: str, value: Any) -> list:
        """
        Load a list of instances of this class populated with all firestore data.
        The condition acceptable values are '<', '<=', '==', '>=', '>' and 'in'.

        Args:
            field (str): The field on firestore document that will be used to filter.
            condition (str): The condition to filter. Example: ==, >=, in.....
            value (Any): The value that must be check.
        """
        return cls.loads_paginated(query=cls.config.collection.where(field, condition, value), order_by=field)

    @classmethod
    def loads_paginated(cls, query: Query = None, fields: list = None, order_by: str = 'firestore_id', limit: int = 500) -> list:
        """
        This will load all documents from a collection using the "limit" number to
        retrieve batches of data, this avoid timeouts from Google API.
        If fields is None, then all fields will be returned.
        The order_by param must be on the fields list.
        If the order_by field does not exist in the document, then the doc will not return.

        Args:
            query (Query, optional): A pre filtered query. Defaults to self.collection.
            fields (list, optional): A list of strings. Defaults to None.
            order_by (str, optional): The name of the field used to sort. Defaults to 'firestore_id'.
            limit (int, optional): The limit of documents that will be retrieved at time. Defaults to 500.

        Raises:
            ValueError: When the order_by is not in the fields.
        """
        if not query:
            query = cls.config.collection

        if fields:
            if order_by in fields:
                # We need to update fields to get the defaults to avoid mistakes
                fields = set(fields)
                fields.update(['firestore_id', 'created_at', 'updated_at'])
                # We sort this to keep always the same order list
                fields = sorted(list(fields))
                query = query.select(field_paths=fields)
            else:
                raise ValueError(f'The order_by ({order_by}) must be in fields({fields}).')

        query = query.order_by(order_by).limit(limit)
        # We load the first batch of data
        docs = [cls(**doc.to_dict()) for doc in query.get()]
        doc_aux = docs
        # If the size of the first batch is equal to the limit that means we have more data to fetch
        while len(doc_aux) == limit:
            last = doc_aux[-1]
            doc_aux = [cls(**doc.to_dict()) for doc in query.start_after(last).get()]
            docs.extend(doc_aux)

        return docs

    # Instance methods
    def get_firestore_id(self) -> str:
        """ Uses the property firestore_id or generate one from UUID4. """
        firestore_id = getattr(self, 'firestore_id', None)
        if not firestore_id:
            firestore_id = uuid4().hex

        return firestore_id

    def load(self) -> None:
        """ Load all data from Firestore for self.firestore_id. """
        doc = self.config.collection.document(self.get_firestore_id()).get()
        if doc.exists:
            # https://everysk.atlassian.net/browse/COD-1818
            # To convert all fields to the correct format we need to pass to _parser_in
            result = self._parser_in(doc.to_dict())
            self.update(result)

    def save(self, merge: bool = True) -> dict:
        """ Save/Update Firestore document, auto update 'updated_at' attribute before save. """
        self.firestore_id = self.get_firestore_id()
        self.updated_at = DateTime.now()
        return self.config.collection.document(self.firestore_id).set(self.to_dict(), merge)

    def to_dict(self) -> dict:
        """ Transform 'self' into a dict using _parse_out method to change some data. """
        ret = BaseDict()
        for key, value in self.items():
            # Discard some keys if needed
            if key not in self.config.excluded_keys:
                ret[key] = self._parser_out(value)

        return ret


class BaseDocumentCachedConfig(BaseDocumentConfig):
    """
    Base class to store the config for DocumentCached instances.
    """
    ## Private attributes
    _cache: RedisCacheCompressed = None

    ## Public attributes
    key_prefix = StrField(default='firestore-document-redis-cached', readonly=True)

    @property
    def cache(self) -> RedisCacheCompressed:
        """ Used to access the cache instance, if we don't have a connection we create one. """
        if self._cache is None:
            self._cache = RedisCacheCompressed()
        return self._cache


class DocumentCached(Document):
    """
    Document that stores data on Redis and Firestore and read data from Redis,
    remember to activate the cloud function that keep the cache synchronized.
    """
    # This need to be configured on child classes
    class Config(BaseDocumentCachedConfig):
        pass

    # We put this here to use the Autocomplete correctly
    config: BaseDocumentCachedConfig = None

    # This is for only get one document and can't be readonly=True
    # because firestore_id is part of the saved document
    firestore_id = StrField(required=True)

    # This key will be used to store the Firestore result in Redis and we need to store it
    # along with the document so that the trigger that syncs Firestore and Redis can use it.
    redis_key = StrField()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.load()
        # This keeps the redis_key hash always updated
        self.redis_key = self.config.cache.get_hash_key(self.get_cache_key())

    def clear_cache_key(self) -> None:
        """ Delete the content from cache. """
        self.config.cache.delete(self.get_cache_key())

    def get_cache_key(self) -> str:
        """ Returns the key that will be used to get/set the cache """
        return f'{self.config.key_prefix}-{self.config.collection_name}-{self.get_firestore_id()}'

    ## Override methods to work with cache
    def load(self) -> None:
        """ Load all data from Redis or Firestore """
        key = self.get_cache_key()
        result = self.config.cache.get(key)
        if result is not None:
            self.update(result)
        else:
            super().load()
            self.config.cache.set(key, self.to_dict())

    def save(self, merge: bool = True):
        """ Removes the key from Redis and update the data on Firestore """
        self.clear_cache_key()
        return super().save(merge)
