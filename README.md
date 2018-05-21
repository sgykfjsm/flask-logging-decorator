# flask-logging-decorator

[![Build Status](https://travis-ci.org/sgykfjsm/flask-logging-decorator.svg?branch=master)](https://travis-ci.org/sgykfjsm/flask-logging-decorator)

This is a deadly simple logging decorator for Flask. This is highly inspired by [canassa/flask-trace](https://github.com/canassa/flask-trace).

## Compatibility

This is tested with Python3.5, 3.6 and Flask1.0.2.

## Installation

```bash
pip install flask-logging-decorator
```

## Run the test

This modules uses [pytest](http://pytest.org/latest/). You can install it before running the test.

```bash
python -m pytest -v
```

## Usage

Import and put it as the decorator function.

```python
import logging

from flask_logging_decorator import trace
from flask import Flask

app = Flask(__name__)

@trace(logging.ERROR)
@app.route('/')
def index():
    return 'hello'

...
```

The application should show the logging message like following.

```text
[2018-05-17 19:01:31,468] ERROR in __init__: trace_uuid=cf66d343-06f4-49cb-a680-59ba9ec77570 method=GET func_name=index func_args: query_args:foo='bar' baz='qux' post_values: trace_info:trace_pathname=main.py trace_lineno=12
```

Note that don't forget to pass the log level argument. You have to pass the appropriate logging level. Otherwise, this decorator never output any messages.

## License

MIT license, see the LICENSE file. You can use this library in open source projects and commercial products.
