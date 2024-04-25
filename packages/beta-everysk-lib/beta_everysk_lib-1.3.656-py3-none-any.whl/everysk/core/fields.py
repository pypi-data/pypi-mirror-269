###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
import re

from collections.abc import Iterator
from sys import maxsize as max_int
from typing import Any, Callable

from everysk.utils import bool_convert

from everysk.core.datetime import DateTime, Date
from everysk.core.exceptions import ReadonlyError, FieldValueError
from everysk.core.object import BaseField

def _min_max_validate(min_value: Any, max_value: Any, value: Any, attr_name: str) -> None:
    """
    Helper function to validate if value is between min and max for fields.

    Args:
        min_value (Any): The min value to be checked.
        max_value (Any): The mas value to be checked.
        value (Any): The value used to validate.
        attr_name (str): The name of the attribute to be used on errors.

    Raises:
        FieldValueError: If the value is not between min and max.
    """
    if value is not None and value is not Undefined:
        min_check = False
        max_check = False

        # Check if min_value and max_value are callable
        min_value = min_value if not callable(min_value) else min_value()
        max_value = max_value if not callable(max_value) else max_value()

        if min_value is not None and min_value is not Undefined:
            min_check = value < min_value

        if max_value is not None and max_value is not Undefined:
            max_check = value > max_value

        if min_check or max_check:
            raise FieldValueError(
                f"The value '{value}' for field '{attr_name}' must be between {min_value} and {max_value}."
            )


class Field(BaseField):
    attr_type: Any = None

    def __init__(
        self,
        default: Any = None,
        required: bool = False,
        readonly: bool = False,
        required_lazy: bool = False,
        empty_is_none: bool = False,
        **kwargs
    ) -> None:
        super().__init__(attr_type=self.attr_type, default=default, required=required, readonly=readonly, required_lazy=required_lazy, empty_is_none=empty_is_none, **kwargs)


class BoolField(Field):
    attr_type: bool = bool

    def clean_value(self, value: Any) -> Any:
        # https://docs.python.org/3/distutils/apiref.html#distutils.util.strtobool
        # The module distutils is deprecated, then we put the function code here
        if value is not None and value is not Undefined:
            value = bool_convert(value)

        return super().clean_value(value)


class ChoiceField(Field):
    attr_type: str = str
    choices: list = None

    def __init__(
        self,
        default: str,
        choices: list,
        readonly: bool = False,
        required: bool = False,
        required_lazy: bool = False,
        empty_is_none: bool = False,
        **kwargs
    ) -> None:
        super().__init__(default=default, required=required, readonly=readonly, choices=choices, required_lazy=required_lazy, empty_is_none=empty_is_none, **kwargs)

        # Choices always need to be a list
        if not self.choices:
            self.choices = []

    def validate(self, attr_name: str, value: Any, attr_type: type = None) -> None:
        """
        Checks if value is in list of choices.
        We discard the value Undefined.

        Raises:
            FieldValueError: If value type don't match with required type.
        """
        if value is not Undefined and value not in self.choices:
            raise FieldValueError(
                f"The value '{value}' for field '{attr_name}' must be in this list {self.choices}."
            )
        super().validate(attr_name, value, attr_type)


class DateField(Field):
    attr_type: Date = Date
    min_date: Date | Callable = None
    max_date: Date | Callable = None

    def __init__(
        self,
        default: Any = None,
        min_date: Date = None,
        max_date: Date = None,
        required: bool = False,
        readonly: bool = False,
        required_lazy: bool = False,
        empty_is_none: bool = False,
        **kwargs
    ) -> None:
        super().__init__(default, min_date=min_date, max_date=max_date, required=required, readonly=readonly, required_lazy=required_lazy, empty_is_none=empty_is_none, **kwargs)

    def clean_value(self, value: Any) -> Any:
        # Convert Date strings to Date object
        if isinstance(value, str):
            if '-' in value:
                value = Date.fromisoformat(value)
            else:
                # Everysk format
                value = Date.strptime(value, '%Y%m%d')

        return super().clean_value(value)

    def validate(self, attr_name: str, value: Any, attr_type: type = None) -> None:
        """
        Checks if value is greater than min and lower than max including both values.
        """
        _min_max_validate(self.min_date, self.max_date, value, attr_name)
        return super().validate(attr_name, value, attr_type)

class DateTimeField(Field):
    attr_type:DateTime = DateTime
    min_date: DateTime | Callable = None
    max_date: DateTime | Callable = None
    force_time: str = None

    def __init__(
        self,
        default: Any = None,
        min_date: DateTime = None,
        max_date: DateTime = None,
        force_time: str = 'FIRST_MINUTE',
        required: bool = False,
        readonly: bool = False,
        required_lazy: bool = False,
        empty_is_none: bool = False,
        **kwargs
    ) -> None:
        super().__init__(default, min_date=min_date, max_date=max_date, force_time=force_time, required=required, readonly=readonly, required_lazy=required_lazy, empty_is_none=empty_is_none, **kwargs)

    def clean_value(self, value: Any) -> Any:
        # Convert DateTime strings to DateTime object
        if isinstance(value, str):
            if not ':' in value:
                value: DateTime = DateTime.fromisoformat(value).force_time(self.force_time)
            else:
                value: DateTime = DateTime.fromisoformat(value)
        elif Date.is_date(value):
            value: DateTime = DateTime.fromisoformat(value.isoformat())

        return super().clean_value(value)

    def validate(self, attr_name: str, value: Any, attr_type: type = None) -> None:
        """
        Checks if value is greater than min and lower than max including both values.
        """
        _min_max_validate(self.min_date, self.max_date, value, attr_name)
        return super().validate(attr_name, value, attr_type)

class DictField(Field):
    attr_type: dict = dict


class FloatField(Field):
    attr_type: float = float
    min_size: float = None
    max_size: float = None

    def __init__(self,
        default: Any = None,
        min_size: float = float('-inf'),
        max_size: float = float('inf'),
        required: bool = False,
        readonly: bool = False,
        required_lazy: bool = False,
        empty_is_none: bool = False,
        **kwargs
    ) -> None:
        super().__init__(default, required, readonly, min_size=min_size, max_size=max_size, required_lazy=required_lazy, empty_is_none=empty_is_none, **kwargs)

    def clean_value(self, value: Any) -> Any:
        # Convert Float strings to float object
        if isinstance(value, (int, str)):
            value = float(value)

        return super().clean_value(value)

    def validate(self, attr_name: str, value: Any, attr_type: type = None) -> None:
        """
        Checks if value is greater than min and lower than max including both values.

        Raises:
            FieldValueError: If value is not between min and max.
        """
        _min_max_validate(min_value=self.min_size, max_value=self.max_size, value=value, attr_name=attr_name)
        return super().validate(attr_name, value, attr_type)


class IntField(Field):
    attr_type: int = int
    min_size: int = None
    max_size: int = None

    def __init__(self,
        default: Any = None,
        min_size: int = -max_int,
        max_size: int = max_int,
        required: bool = False,
        readonly: bool = False,
        required_lazy: bool = False,
        empty_is_none: bool = False,
        **kwargs
    ) -> None:
        super().__init__(default, required, readonly, min_size=min_size, max_size=max_size, required_lazy=required_lazy, empty_is_none=empty_is_none, **kwargs)

    def clean_value(self, value: Any) -> Any:
        # Convert Int strings to int object
        if isinstance(value, str):
            value = int(value)

        return super().clean_value(value)

    def validate(self, attr_name: str, value: Any, attr_type: type = None) -> None:
        """
        Checks if value is greater than min and lower than max including both values.

        Raises:
            FieldValueError: If value is not between min and max.
        """
        _min_max_validate(min_value=self.min_size, max_value=self.max_size, value=value, attr_name=attr_name)
        return super().validate(attr_name, value, attr_type)


class IteratorField(Field):
    attr_type: Iterator = Iterator

    def clean_value(self, value: Any) -> Any:
        # Convert List/Str to iterators
        if isinstance(value, (list, str)):
            value = iter(value)

        return super().clean_value(value)


class ListField(Field):
    attr_type: list = list
    min_size: int = None
    max_size: int = None

    def __init__(
        self,
        default: Any = None,
        min_size: int = 0,
        max_size: int = max_int,
        readonly: bool = False,
        required: bool = False,
        required_lazy: bool = False,
        empty_is_none: bool = False,
        **kwargs
    ) -> None:
        if min_size < 0:
            raise FieldValueError('List min_size cloud not be a negative number.')
        super().__init__(default=default, min_size=min_size, max_size=max_size, readonly=readonly, required=required, required_lazy=required_lazy, empty_is_none=empty_is_none, **kwargs)

    def clean_value(self, value: Any) -> Any:
        # Insert value in list if value is an Str instance.
        if isinstance(value, str):
            value = [value]

        return super().clean_value(value)

    def validate(self, attr_name: str, value: Any, attr_type: type = None) -> None:
        """
        Checks if value is greater than min_size and lower than max_size including both values.

        Raises:
            FieldValueError: If value is not list instance.
            FieldValueError: If value is not between min_size and max_size.
        """
        if value is not None and value is not Undefined:
            if not isinstance(value, list):
                raise FieldValueError(f"The '{attr_name}' value must be a list.")
            if not self.min_size <= len(value) <= self.max_size:
                raise FieldValueError(
                    f"The attribute '{attr_name}' is not within the specified list range. min_size: {self.min_size} max_size: {self.max_size}"
                )
        super().validate(attr_name, value, attr_type)

class StrField(Field):
    attr_type: str = str
    min_size: int = None
    max_size: int = None
    regex: re.Pattern = None

    def __init__(
        self,
        default: Any = None,
        min_size: int = 0,
        max_size: int = max_int,
        regex: str = None,
        readonly: bool = False,
        required: bool = False,
        required_lazy: bool = False,
        empty_is_none: bool = False,
        **kwargs
    ) -> None:
        if min_size < 0:
            raise FieldValueError('String min_size cloud not be a negative number.')
        super().__init__(default=default, regex=regex, min_size=min_size, max_size=max_size, readonly=readonly, required=required, required_lazy=required_lazy, empty_is_none=empty_is_none, **kwargs)

    def validate(self, attr_name: str, value: Any, attr_type: type = None) -> None:
        """
        Checks if value is greater than min_size and lower than max_size including both values.

        Raises:
            FieldValueError: If value is not str instance.
            FieldValueError: If value is not between min_size and max_size.
        """
        # First let all default checks be done.
        super().validate(attr_name, value, attr_type)

        if self.regex and value and value is not Undefined and not self.regex.match(value):
            raise FieldValueError(
                f"The value '{value}' for field '{attr_name}' must match with this regex: {self.regex.pattern}."
            )

        # Then we check for the size.
        try:
            if value is not None and value is not Undefined:
                _min_max_validate(min_value=self.min_size, max_value=self.max_size, value=len(value), attr_name=attr_name)
        except FieldValueError as error:
            raise FieldValueError(
                f"The length '{len(value)}' for attribute '{attr_name}' must be between '{self.min_size}' and '{self.max_size}'."
            ) from error

class RegexField(Field):
    attr_type: re.Pattern = re.Pattern

    def __init__(
        self,
        default: Any = None,
        readonly: bool = False,
        required: bool = False,
        required_lazy: bool = False,
        empty_is_none: bool = False,
        **kwargs
    ) -> None:
        super().__init__(default=default, readonly=readonly, required=required, required_lazy=required_lazy, empty_is_none=empty_is_none, **kwargs)

    def clean_value(self, value: Any) -> Any:
        # Insert value in list if value is an Str instance.
        if isinstance(value, str):
            value = re.compile(value)
        return super().clean_value(value)

class TupleField(Field):
    attr_type: tuple = tuple


## Readonly Fields
def _do_nothing(*args, **kwargs):
    #pylint: disable=unused-argument
    raise ReadonlyError('This field value cannot be changed.')

class ReadonlyDictField(DictField):

    class ReadonlyDict(dict):
        __setitem__ = _do_nothing
        __delitem__ = _do_nothing
        pop = _do_nothing
        popitem = _do_nothing
        clear = _do_nothing
        update = _do_nothing
        setdefault = _do_nothing

    def __init__(
        self,
        default: Any,
        readonly: bool = True,
        required: bool = False,
        required_lazy: bool = False,
        empty_is_none: bool = False,
    ) -> None:
        # Transform the dict received to Readonly.
        # This is to block internals updates to data in default dict.
        if default is not None and default is not Undefined:
            default = self.ReadonlyDict(default)

        super().__init__(default=default, required=required, readonly=readonly, required_lazy=required_lazy, empty_is_none=empty_is_none)


class ReadonlyListField(ListField):

    class ReadonlyList(list):
        __setitem__ = _do_nothing
        __delitem__ = _do_nothing
        append = _do_nothing
        clear = _do_nothing
        extend = _do_nothing
        insert = _do_nothing
        pop = _do_nothing
        remove = _do_nothing
        reverse = _do_nothing
        sort = _do_nothing

    def __init__(
        self,
        default: Any,
        readonly: bool = True,
        required: bool = False,
        required_lazy: bool = False,
        empty_is_none: bool = False,
    ) -> None:
        # Transform the list received to Readonly.
        # This is to block internals updates to data in default list.
        if default is not None and default is not Undefined:
            default = self.ReadonlyList(default)

        super().__init__(default=default, required=required, readonly=readonly, required_lazy=required_lazy, empty_is_none=empty_is_none)
