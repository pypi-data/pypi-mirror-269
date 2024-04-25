
# Everysk Lib

Everysk's library was developed with the aim of unifying python
codes to be used in various company projects.


## Docker

To run the pypi server:

```bash
  docker build --file ./docker/Dockerfile --target everysk_pypi_server --tag everysk_pypi_server:latest .
  docker run --rm -it -e PYPI_PASSWORD='123123' -p 0.0.0.0:8080:80 -p 0.0.0.0:2020:22 everysk_pypi_server:latest
```

To build the library and send to Pypi server:

```bash
  docker build --file ./docker/Dockerfile --target everysk_lib_build --tag everysk_lib_build:latest .
  docker run --rm -it -e PYPI_PASSWORD='123123' -e PYPI_HOST='192.168.0.116' everysk_lib_build:latest

```

## Usage/Examples

Module object and fields are used to create class with consistent data.

```python
    >>> from everysk.core.fields import BoolField
    >>> from everysk.core.object import BaseDict
    >>>
    >>> class MyClass(BaseDict):
    ...     field: BoolField(required=True)
    >>>
    >>> obj = MyClass(field=True)
    >>> obj.field is True
    ... True
    >>> obj.field == obj['field']
    ... True

```

Module http has connection base class to use on HTTP Methods.

```python
    >>> from everysk.core.http import HttpGETConnection
    >>>
    >>> class MyConnection(HttpGETConnection):
    ...     url: StrField(defautl='https://example.com', readonly=True)
    ...     def get_params(self) -> dict:
    ...         # Will be added to url p=1&p=2
    ...         return {'p': 1, 'p': 2}
    ...
    ...     def message_error_check(self, message: str) -> bool:
    ...         # If this message appear on HttpError then we try again.
    ...         return 'server is busy' in message
    >>>
    >>> response = MyConnection().get_response()

```

Module settings is the sum of all settings.py created on the project.
Every setting will have it's value first from env otherwise from the attribute.

```python
    >>> from everysk.core.config import settings
    >>> settings.DEBUG
    True

```

Module firestore.DocumentCached is a Redis/Firestore document. This uses Redis for
read the data and Redis/Firestore to store the data. To keep the cache synchronized
with Firestore, use everysk/cloud_function. With this when we alter the data using
Firestore interface the cache will be updated.

```python
    >>> from everysk.core.firestore import DocumentCached
    >>> doc = Document(_collection_name='collection', firestore_id='firestore_id')
    >>> doc.firestore_id
    'firestore_id'

```

## Installation

Install everysk-lib with pip:

```bash
  pip install --index-url https://PYPI_HOST everysk-lib

```


## Running Tests

To run tests, run the following command in development VS Code environment:

```bash
  ./run.sh tests
```

Once this lib is installed from pypi on your project, to run tests use:

```bash
  python3 -m unittest everysk.core.tests
```


## Running Tests with coverage

To run tests with coverage report, run the following command:

```bash
  ./run.sh coverage
```


## Contributing

Contributions are always welcome!

Clone this repo from GIT and use it in VS Code with Dev Containers extension.


## License

(C) Copyright 2023 EVERYSK TECHNOLOGIES

This is an unpublished work containing confidential and proprietary
information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
without authorization of EVERYSK TECHNOLOGIES is prohibited.

Date: Jan 2023

Contact: contact@everysk.com

URL: https://everysk.com/
