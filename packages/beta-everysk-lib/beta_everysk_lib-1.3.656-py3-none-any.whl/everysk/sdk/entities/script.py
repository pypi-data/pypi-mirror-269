###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

###############################################################################
#   Imports
###############################################################################
from typing import Any, Callable

from everysk.sdk.base import BaseSDK
###############################################################################
#   Base Script Implementation
###############################################################################
class Script(BaseSDK):
    """
    A base class for scripted queries.
    This class provides a base implementation for scripted queries.

    Attributes:
        - _klass (callable): The class to instantiate when fetching an entity.

    Example usage:
        To fetch an entity:
        >>> script = Script(klass=MyEntity)
        >>> entity = script.fetch(user_input, variant, workspace)
    """
    _klass: Callable = None

    def __init__(self, klass: Callable) -> None:
        super().__init__(_klass=klass)
        self._klass = klass

    def fetch(self, user_input: Any, variant: str, workspace: str) -> Any:
        """
        Process a scripted query based on user input, variant, and workspace.

        This method provides a way to construct and execute different types of queries
        based on the specified variant. It's designed to handle a variety of scenarios
        and return the desired entity or entities based on the input parameters.

        Parameters:
            - user_input (Any): The input provided by the user, which can be used for filtering
            or as a direct entity ID.
            - variant (str): The type of scripted query to execute. Determines how the method
            processes the user input and constructs the query. Supported variants include
            'previousWorkers', 'tagLatest', any string starting with 'select', and potentially
            others.
            - workspace (str): The workspace context for the query. Used for scoping and
            verifying entity retrieval.

        Returns:
            - Any: Depending on the variant and user input, the method might return an entity,
            a list of entities, or None.

        Raises:
            - ValueError: If there's an attempted cross-workspace operation or other variant-specific
            error conditions are met.

        Note:
            The method behavior can vary greatly depending on the `variant` parameter, and it's
            important to ensure that the variant aligns with the expected user input structure.

        Example usage:
            To fetch an entity:
            >>> script = Script(klass=MyEntity)
            >>> entity = script.fetch(user_input, variant, workspace)
        """
        if user_input is None:
            return None

        if variant == 'previousWorkers' and user_input.get('id') is None:
            return self._klass(**user_input)

        return self.get_response(self_obj=self, params={'user_input': user_input, 'variant': variant, 'workspace': workspace})

    def persist(self, entity: Any, persist: str) -> Any:
        """
        This method provides a way to persist an entity based on the specified persist type.

        Parameters:
            - entity (Any): The entity to persist.
            - persist (str): The type of persist to execute. Determines how the method
            persists the entity. Supported persists include 'insert', 'update', and 'delete'.

        Returns:
            - Any: Depending on the persist type, the method might return an entity.

        Example usage:
            To persist an entity:
            >>> script = Script(klass=MyEntity)
            >>> entity = script.persist(entity, persist)
        """
        return self.get_response(self_obj=self, params={'entity': entity, 'persist': persist})
