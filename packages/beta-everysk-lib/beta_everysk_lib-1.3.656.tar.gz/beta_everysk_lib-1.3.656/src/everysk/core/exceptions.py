###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
class _BaseException(Exception):
    """
    Custom Base Exception that will generate an attribute called msg
    with the error message and will be used to catch errors.
    """
    ## Private attributes
    _args: tuple = None

    ## Public attributes
    msg: str = 'Application error.'

    ## Properties
    @property
    def args(self) -> tuple:
        """ Keeps the args attribute in sync with the msg attribute. """
        return self._args

    @args.setter
    def args(self, value: tuple) -> None:
        """  Used to keep sync the args and the msg attribute. """
        if not isinstance(value, tuple):
            raise ValueError(f"The 'args' value must be a tuple not {type(value)}.")

        self.msg = value[0]
        self._args = value

    ## Methods
    def __init__(self, *args: list, **kwargs: dict) -> None:
        super().__init__(*args)
        if len(args) == 1:
            self.msg = args[0]

        if kwargs:
            for attr, value in kwargs.items():
                setattr(self, attr, value)

    def __str__(self):
        return f'{self.msg}'


class DateError(_BaseException):
    pass


class DefaultError(_BaseException):
    pass


class FieldValueError(_BaseException, ValueError):
    pass


class EntityNotFound(_BaseException):
    pass

class HttpError(_BaseException):
    status_code: int = 500

    def __str__(self):
        return f'{self.status_code} -> {self.msg}'


class ReadonlyError(_BaseException):
    pass


class RedisEmptyListError(_BaseException):
    pass


class RequiredError(_BaseException):
    pass

class SDKError(_BaseException):
    pass

class QueryError(_BaseException):
    pass

class EntityError(_BaseException):
    pass
