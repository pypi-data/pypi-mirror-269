###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from copy import copy, deepcopy
from inspect import isroutine
from typing import Any, Self

from everysk.core.datetime import DateTime, Date
from everysk.core.exceptions import DefaultError, RequiredError, FieldValueError


def __get_field_value__(obj: Any, attr: str, value: Any) -> Any:
    """
    Function that get the cleaned value for a Field and validate this value.

    Args:
        obj (Any): A class or a instance of BaseObject.
        attr (str): The attribute name.
        value (Any): The value that is assigned to this attribute.

    Raises:
        FieldValueError: If we find validation errors.
    """
    # Get all attributes that the object has
    attributes = getattr(obj, MetaClass._attr_name) # pylint: disable=protected-access
    try:
        field = attributes[attr]
    except KeyError:
        return value

    # field can be the type itself or an instance of BaseField
    if isinstance(field, BaseField):
        try:
            value = field.get_cleaned_value(value)
        except Exception as error:
            # Add attribute name to error
            error.args = (f'{attr}: {str(error)}',)
            raise FieldValueError(error.args) from error

        field.validate(attr, value)
    else:
        _validate(attr, value, field)

    return value


def _required(attr_name: str, value: Any) -> None:
    """
    Checks if value is required, required values can't be: None, '', [], {}.

    Raises:
        RequiredError: When value is required and match with False conditions.
    """
    if value in (Undefined, None, '', (), [], {}):
        raise RequiredError(f'The {attr_name} attribute is required.')


def _validate(attr_name: str, value: Any, attr_type: type) -> None:
    """
    Checks if value is of value_type.

    Raises:
        FieldValueError: When value is not of value_type.
    """
    if attr_type is Any:
        return None
    elif attr_type is callable:
        check = callable(value)
    else:
        check = value is None or value is Undefined or (attr_type == Date and Date.is_date(value)) or (attr_type == DateTime and DateTime.is_datetime(value)) or isinstance(value, attr_type)

    if check is False:
        raise FieldValueError(f'Key {attr_name} must be {attr_type}.')


class BaseField:
    """ Base class of all fields that will guarantee their type. """
    ## Public attributes
    attr_type: type = None
    default: Any = None
    readonly: bool = False
    required: bool = False
    required_lazy: bool = False
    empty_is_none: bool = False

    def __init__(
        self,
        attr_type: type,
        default: Any = None,
        readonly: bool = False,
        required: bool = False,
        required_lazy: bool = False,
        empty_is_none: bool = False,
        **kwargs
    ) -> None:
        """
        Use kwargs to set more attributes on the Field.

        Raises:
            DefaultError: For default values they can't be empty [] or {}.
            RequiredError: If field is readonly, then default value is required.
        """
        self.attr_type = attr_type
        if required and required_lazy:
            raise FieldValueError("Required and required_lazy can't be booth True.")

        self.required = required
        self.required_lazy = required_lazy

        if default is not None and not default and isinstance(default, (list, dict)):
            # For default values they can't be empty [] or {} - because this can cause
            # some issues with class attributes where these type can aggregate values.
            raise DefaultError('Default value cannot be a list or a dict.')

        if readonly and (default is None or default is Undefined):
            raise RequiredError('If field is readonly, then default value is required.')

        self.readonly = readonly

        # We use this flag to convert '' to None
        self.empty_is_none = empty_is_none

        # Other attributes will be assigned directly
        for key, value in kwargs.items():
            setattr(self, key, value)

        # For the last We need to store the cleaned value
        self.default = self.get_cleaned_value(default)

    def __repr__(self) -> str:
        return self.__class__.__name__

    def __eq__(self, obj: object) -> bool:
        """
        One field will be equal to another one if all attributes are the same.

        Args:
            obj (object): The obj for compare.
        """
        return self.__dict__ == obj.__dict__

    def transform_to_none(self, value: Any) -> Any:
        """
        Transforms value to None if needed.
        """
        if self.empty_is_none and value == '':
            value = None

        return value

    def get_cleaned_value(self, value: Any) -> Any:
        # We first verify if we need to transform the value to None
        value = self.transform_to_none(value)

        # Then we run the get_value method when value is a callable
        value = self.get_value(value)

        # Then we run the clean_value method
        value = self.clean_value(value)

        return value

    def get_value(self, value: Any) -> Any:
        """
        Must be implemented in child classes that need do some changes
        on received value before clean_value.
        """
        # If value is callable we call it
        if callable(value):
            value = value()
        return value

    def clean_value(self, value: Any) -> Any:
        """
        Must be implemented in child classes that need do some
        changes on received value.
        """
        return value

    def validate(self, attr_name: str, value: Any, attr_type: type = None) -> None:
        """
        Checks if value is required and if is of correct type.

        Raises:
            RequiredError: If required and None is passed
            FieldValueError: If value type don't match with required type.
        """
        if attr_type is None:
            attr_type = self.attr_type

        if self.readonly:
            # This is necessary to be able to at least assign the default value to the field
            if value != self.default:
                raise FieldValueError(f"The field '{attr_name}' value cannot be changed.")

        if self.required and not self.required_lazy:
            _required(attr_name, value)

        _validate(attr_name, value, attr_type)

    def __getattr__(self, name: str) -> Any:
        """
        This method is used to handle pylint errors where the method/attribute does not exist.
        The problem is that we change the field in the MetaClass to the Field's default value,
        so StrField does not have the str methods but the result is a string.
        This method will only be executed if the method/attributes do not exist in the Field class.

        Args:
            name (str): The name of the method/attribute.
        """
        # https://pythonhint.com/post/2118347356810295/avoid-pylint-warning-e1101-instance-of-has-no-member-for-class-with-dynamic-attributes
        return getattr(self.attr_type, name)


class MetaClass(type):
    _attr_name: str = '__attributes__'
    _anno_name: str = '__annotations__'

    def __new__(mcs, name: str, bases: tuple, attrs: dict) -> type:
        """
        This method is executed every time a BaseObject Class is created in the Python runtime.
        We changed this method to create the config and attributes properties and update the annotations.

        Example:

            >>> from everysk.core.object import BaseObject
            >>> class MyClass(BaseDict):
            ...     class Config:
            ...         value: int = 1

            >>> obj1 = MyClass()
            >>> obj2 = MyClass()
            >>> MyClass.config.value, obj1.config.value, obj2.config.value
            (1, 1, 1)

            >>> obj1.config.value = 3
            >>> MyClass.config.value, obj1.config.value, obj2.config.value
            (3, 3, 3)

            >>> MyClass.Config
            ---------------------------------------------------------------------------
            AttributeError                            Traceback (most recent call last)
            ----> 1 MyClass.Config

            AttributeError: type object 'MyClass' has no attribute 'Config'

        Args:
            mcs (type): Represents this class.
            name (str): The name for the new class.
            bases (tuple): All inheritance classes.
            attrs (dict): All attributes that the new class has.

        Returns:
            type: Return the new class object.
        """
        # Creating the config property.
        try:
            Config = attrs.pop('Config') # pylint: disable=invalid-name
            attrs['config'] = Config()
        except KeyError:
            pass

        # We need all attributes to validate the types later
        # So we need to get the parents attributes too
        attributes = {}
        for parent in bases:
            attributes.update(getattr(parent, mcs._attr_name, {}))

        # We could not update the info inside the original attrs dict because:
        # RuntimeError: dictionary changed size during iteration
        # So we remove the attributes that we need to update
        attributes.update(attrs.pop(mcs._attr_name, {}))
        annotations: dict = attrs.pop(mcs._anno_name, {})
        new_attrs = {}
        for attr_name, attr_value in attrs.items():
            # We discard all python dunder attributes, all functions, all properties, Undefined and None values
            if not attr_name.startswith('__') and \
               not isroutine(attr_value) and \
               not isinstance(attr_value, property) and \
               attr_value is not None and \
               attr_value is not Undefined:
                # For BaseFields we need to use the properties and set the correct value in the attribute
                if isinstance(attr_value, BaseField):
                    # We keep a copy of the value inside the __attributes__
                    attributes[attr_name] = attr_value

                    # We set the correct value to this attribute in the class
                    new_attrs[attr_name] = attr_value.default

                    # We create the annotation for this attribute
                    if attr_name not in annotations:
                        annotations[attr_name] = attr_value.attr_type
                else:
                    # For normal attributes we only store the class
                    attributes[attr_name] = type(attr_value)

                    # Now we update annotations for attributes that are not annotated
                    # Ex: var = 1
                    if attr_name not in annotations:
                        annotations[attr_name] = type(attr_value)

        # With both completed now we need to get the fields that are only annotations
        # class MyClass:
        #     var: str
        for key in annotations.keys() - attributes.keys():
            attributes[key] = annotations[key]
            # We set the default value to None to avoid break the code
            new_attrs[key] = None

        # Then we update the attributes list for this new class
        attrs[mcs._attr_name] = attributes
        attrs[mcs._anno_name] = annotations
        attrs.update(new_attrs)

        return super().__new__(mcs, name, bases, attrs)

    def __setattr__(cls, __name: str, __value: Any) -> None:
        """
        Method that sets the values on fields of the class.

        Args:
            __name (str): The attribute name.
            __value (Any): The value that is set.
        """
        return super().__setattr__(__name, __get_field_value__(cls, __name, __value))


class BaseObject(metaclass=MetaClass):
    """
    To ensure correct check for data keys
    uses https://docs.python.org/3/library/typing.html standards.

        >>> from utils.object import BaseObject
        >>> class MyObject(BaseObject):
        ...     var_int: int = None
        ...
        >>> obj = MyObject(var_int='a')
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "/var/app/utils/object.py", line 151, in __init__
            setattr(self, key, value)
        File "/var/app/utils/object.py", line 209, in __setattr__
            value = self.__get_clean_value__(__name, value)
        File "/var/app/utils/object.py", line 192, in __get_clean_value__
            _validate(attr, value, annotations[attr])
        File "/var/app/utils/object.py", line 56, in _validate
            raise DataTypeError(f'Key {attr_name} must be {attr_type}.')
        utils.exceptions.DataTypeError: Key var_int must be <class 'int'>.
    """
    _is_frozen: bool = False # This will control if we can update data on this class

    def __init__(self, **kwargs) -> None:
        # Validate all required fields
        attributes = self.__get_attributes__()
        for attr_name, field in attributes.items():
            if getattr(field, 'required', False):
                _required(attr_name=attr_name, value=kwargs.get(attr_name))

        # Set all kwargs on the object
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Set the instance to be Frozen
        try:
            self._is_frozen = self.config.frozen
        except AttributeError:
            pass

    def __check_frozen__(self) -> None:
        """
        Method that checks if this class is a Frozen object and raises attribute error.
        """
        if self._is_frozen:
            raise AttributeError(f'Class {self.get_full_doted_class_path()} is frozen and cannot be modified.')

    def __copy__(self) -> Self:
        """
        A shallow copy constructs a new compound object and then (to the extent possible)
        inserts references into it to the objects found in the original.
        If the object is Frozen the copy will not be.
        This method is used when we call copy(obj).
        """
        # We need to copy the __dict__
        obj = copy(self.__dict__)

        # We must not copy the config attribute
        obj.pop('config', None)

        # We create a new obj
        obj = type(self)(**obj)
        return obj

    def __deepcopy__(self, memo: dict = None) -> Self:
        """
        A deep copy constructs a new compound object and then, recursively,
        inserts copies into it of the objects found in the original.
        This method is used when we call deepcopy(obj).

        Args:
            memo (dict, optional): A memory object to avoid copy twice. Defaults to None.
        """
        # We need to copy the __dict__
        obj = deepcopy(self.__dict__, memo)

        # We must not copy the config attribute
        obj.pop('config', None)

        # We create a new obj
        obj = type(self)(**obj)
        return obj

    def __delattr__(self, __name: str) -> None:
        """
        Method that removes __name from the object.

        Args:
            __name (str): The name of the attribute that will be removed.

        Raises:
            AttributeError: If is frozen.
        """
        self.__check_frozen__()
        super().__delattr__(__name)

    def __get_attributes__(self) -> dict:
        """
        Get all attributes from this class.
        """
        return getattr(self, MetaClass._attr_name) # pylint: disable=protected-access

    def __get_clean_value__(self, attr: str, value: Any) -> Any:
        """
        Pass value to a clean function and checks if value match's the correct type.

        Raises:
            FieldValueError: If value and type don't match the correct type.
        """
        return __get_field_value__(self, attr, value)

    def __getstate__(self) -> dict:
        """
        This method is used by Pickle module to get the correct serialized data.
        We need to remove the config attribute from the serialized data
        so we can recreate the object later.
        https://docs.python.org/3.11/library/pickle.html#handling-stateful-objects
        """
        dct = self.__dict__.copy()
        try:
            del dct['config']
        except KeyError:
            pass

        return dct

    def __setattr__(self, __name: str, __value: Any) -> None:
        """
        Method changed from BaseClass for check de integrity of data.
        This method is executed on setting attributes in the object.
        Ex: obj.attr = 1

        Raises:
            AttributeError: If is frozen.
        """
        self.__check_frozen__()
        super().__setattr__(__name, self.__get_clean_value__(__name, __value))

    @classmethod
    def __set_attribute__(cls, attr_name: str, attr_type: Any, attr_value: Any) -> None:
        """
        Method that updates the list of attributes/annotations for this class.
        Normally this is used to update a class after it was created.

        Args:
            attr_name (str): The name for the new attribute.
            attr_type (Any): The type for the new attribute.
            attr_value (Any): The value for the new attribute.
        """
        attributes = getattr(cls, MetaClass._attr_name, {}) # pylint: disable=protected-access
        annotations = getattr(cls, MetaClass._anno_name, {}) # pylint: disable=protected-access
        try:
            # For BaseFields
            annotations[attr_name] = attr_type.attr_type
        except AttributeError:
            # Normal types
            annotations[attr_name] = attr_type

        attributes[attr_name] = attr_type
        # After we set the attributes/annotations we set the value in the class
        setattr(cls, attr_name, attr_value)

    ## Public methods
    def get_full_doted_class_path(self):
        """
        Return full doted class path to be used on import functions.
        Example:
            'everysk.core.BaseObject'
        """
        return f'{self.__module__}.{self.__class__.__name__}'

    def replace(self, **changes) -> Self:
        """
        Creates a new object of the same type as self, replacing fields with values from changes.

        Example:

            >>> from everysk.core.object import BaseObject
            >>> obj = BaseObject(attr=1)
            >>> obj.attr
            1
            >>> copy = obj.replace(attr=2)
            >>> copy.attr
            2

        Args:
            **changes (dict): All named params that are passed to this method.

        Returns:
            Self: A copy of this object with the new values.
        """
        obj = deepcopy(self.__dict__)

        # We must not copy the config attribute
        obj.pop('config', None)

        obj.update(changes)
        return type(self)(**obj)

    def validate_required_fields(self) -> None:
        """
        Try to validate all fields that are checked with required_lazy, because fields with
        required are always validate on the init.
        """
        attributes = self.__get_attributes__()
        for attr_name, field in attributes.items():
            if getattr(field, 'required_lazy', False):
                _required(attr_name=attr_name, value=getattr(self, attr_name, None))


class BaseDict(BaseObject, dict):
    """
    Extends BaseObject and also guarantees that BaseDict['key'] is equal to BaseDict.key

        >>> from utils.object import BaseDict
        >>> class MyDict(BaseDict):
        ...     var_int: int = None
        ...
        >>> obj = MyDict(var_int='test')
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "/var/app/utils/object.py", line 151, in __init__
            raise DataTypeError(f'Key {attr_name} must be {attr_type}.')
        File "/var/app/utils/object.py", line 279, in __setattr__
            if key.startswith('_'):
        File "/var/app/utils/object.py", line 209, in __setattr__
            DataTypeError: If value and type don't match the correct type.
        File "/var/app/utils/object.py", line 192, in __get_clean_value__
            # Create base annotations
        File "/var/app/utils/object.py", line 56, in _validate
            elif isinstance(value, attr_type):
        utils.exceptions.DataTypeError: Key var_int must be <class 'int'>.
        >>> obj = MyDict(var_int=10)
        >>> obj['var_int'] == obj.var_int
        True
    """
    _keys_blacklist: frozenset[str] = frozenset(['config'])

    ## Private Methods
    def __init__(self, **kwargs) -> None:
        ## After init we need to get all key/values from parents and set to the instance
        # Copy generates infinite recursion
        attributes = self.__get_attributes__()
        for key in attributes.keys() - kwargs.keys():
            if self.is_valid_key(key=key):
                # On init, attributes has value because inheritance
                # we are just updating the values of the keys
                # self['key'] is None but self.key has value
                self[key] = self[key]

        super().__init__(**kwargs)

    def __delattr__(self, name: str, caller: str = None) -> None:
        """
        Removes an atribute from self.

        Args:
            name (str): The attribute that will be removed.
            caller (str, optional): Used to avoid recursion when internally called. Defaults to None.

        Raises:
            AttributeError: If the attribute is not found.
        """
        # Remove attribute
        super().__delattr__(name)

        # Caller not None means this method was called from __delitem__
        # then we do not call the method again avoiding infinite loop
        if caller is None:
            try:
                # Some times the attribute will not exists
                self.__delitem__(name, caller='__delattr__')
            except KeyError:
                pass

    def __delitem__(self, key: Any, caller: str = None) -> None:
        """
        Removes an key from self.

        Args:
            key (Any): The key that will be removed.
            caller (str, optional): Used to avoid recursion when internally called. Defaults to None.

        Raises:
            KeyError: If the key is not found.
        """
        # Remove key
        super().__delitem__(key)

        # Caller not None means this method was called from __delattr__
        # then we do not call the method again avoiding infinite loop
        if caller is None:
            self.__delattr__(key, caller='__delitem__')

    def __getitem__(self, key: str) -> Any:
        """
        Get key from self or search on a parent.

        Args:
            key (str): The key name to search.

        Raises:
            KeyError: If the key does not exist.
        """
        if self.is_valid_key(key=key):
            try:
                return super().__getitem__(key)
            except KeyError:
                pass

            try:
                return getattr(self, key)
            except AttributeError:
                pass

        raise KeyError(key) # pylint: disable=raise-missing-from

    def __setattr__(self, name: str, value: Any, caller: str = None) -> None:
        """
        Method changed from BaseClass for guarantee de integrity of data attributes.
        This method is executed on setting attributes in the object.
        Ex: obj.attr = 1

        Raises:
            AttributeError: If is frozen.
        """
        super().__setattr__(name, value)
        # Because self.__get_clean_value__ can change the value we need to pick it from self
        new_value = getattr(self, name)

        # When value is associated:
        # directly on the key Ex dict['key'] = value then caller will be __setitem__
        # directly on attribute Ex dict.key = value then caller will be None
        # Don't do that to private attributes
        if caller is None and self.is_valid_key(key=name):
            # For integrity guarantee writes the value to the dictionary key as well.
            self.__setitem__(name, new_value, caller='__setattr__')

    def __setitem__(self, key: str, item: Any, caller: str = None) -> None:
        """
        Method changed from BaseClass for guarantee de integrity of data keys.
        This method is executed on setting items in the dictionary.
        Ex: d = dict(key=1) or d['key'] = 1

        Raises:
            AttributeError: If is frozen.
        """
        if key.startswith('_'):
            raise KeyError("Keys can't start with '_'")

        if key in self._keys_blacklist:
            raise KeyError(f'The key cannot be called "{key}".')

        # When value is associated:
        # directly on the key Ex dict['key'] = value then caller will be None
        # directly on attribute Ex dict.key = value then caller will be __setattr__
        if caller is None:
            # For integrity guarantee writes the value to the attribute as well.
            self.__setattr__(key, item, caller='__setitem__')

            # The setattr can "clean" the value them we need to catch it again
            item = getattr(self, key)

        # If key is a property we do not set on dict
        if not isinstance(getattr(self.__class__, key, None), property):
            super().__setitem__(key, item)

    def is_valid_key(self, key: str) -> bool:
        """
        This method checks if the key is valid.
        Valid keys are the ones that not starts with '_' and
        are not in the self._keys_blacklist.

        Args:
            key (str): The key that needs to be checked.
        """
        return not key.startswith('_') and key not in self._keys_blacklist

    ## Public Methods
    def clear(self) -> None:
        """
        This method clears the dictionary.

        Raises:
            AttributeError: If is frozen.
        """
        self.__check_frozen__()
        # Because we integrate key/attributes we need to remove booth
        # The original clear only remove keys
        # We need to convert keys to a list, because the original is a iterator
        for key in list(self.keys()):
            del self[key]

    def copy(self) -> dict:
        """
        Generate a copy for this object, we need to use deepcopy because
        this object could have some keys/attributes and they need to be on the copy.
        If the object is Frozen, the copy will not be.
        """
        return deepcopy(self)

    def fromkeys(self, keys: list, default: Any = None) -> dict:
        """
        Create a new object with the keys, if key does not exists add one with default value.
        If the object is Frozen, the copy will not be.

        Args:
            keys (list): The list with the keys for the new object.
            default (Any, optional): The default value if the key does not exists. Defaults to None.
        """
        # Create a new key list with all keys and use a set to avoid duplicates
        keys_aux = set(keys)
        keys_aux.update(self.keys())

        dct = self.copy()
        for key in keys_aux:
            if key in keys:
                dct[key] = dct.get(key, default)
            else:
                del dct[key]

        return dct

    def pop(self, *args) -> Any:
        """
        Remove specified key and return the corresponding value.
        If the key is not found return the default otherwise raise a KeyError.

        Args:
            key (str): The key that will be removed.
            default (Any, optional): The default value if key is not found.

        Raises:
            AttributeError: If is frozen.
            KeyError: If the default is not passed and key is not found.
        """
        self.__check_frozen__()
        ret = super().pop(*args)

        try:
            # Some times the attribute will not exists
            self.__delattr__(args[0]) # pylint: disable=unnecessary-dunder-call
        except AttributeError:
            pass

        return ret

    def popitem(self) -> tuple:
        """
        Remove and return a (key, value) pair as a 2-tuple.
        Pairs are returned in LIFO (last-in, first-out) order.

        Raises:
            AttributeError: If is frozen.
            KeyError: If the dict is empty.
        """
        self.__check_frozen__()
        return super().popitem()

    def update(self, *args, **kwargs) -> None:
        """
        Refactor to use __setitem__ and perform correct checks on data.
        https://stackoverflow.com/a/2588648
        https://stackoverflow.com/a/2390889

        Raises:
            AttributeError: If is frozen.
        """
        self.__check_frozen__()
        for key, value in dict(*args, **kwargs).items():
            self[key] = value
