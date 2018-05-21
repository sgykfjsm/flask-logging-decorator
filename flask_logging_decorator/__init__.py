from functools import wraps
import inspect
import logging
from typing import Callable, List, Dict
from reprlib import Repr
from uuid import uuid4

__all__ = ['trace']

__r = Repr()
__r.maxarray = __r.maxarray * 10
__r.maxdict = __r.maxdict * 10
__r.maxstring = __r.maxstring * 10


def __get_trace_uuid() -> str:
    from flask import g

    if not hasattr(g, 'trace_uuid'):
        g.trace_uuid = str(uuid4())

    return g.trace_uuid


def trace(level: int=logging.NOTSET) -> Callable:
    # from pytest import set_trace; set_trace()
    def outer(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args: List, **kwargs: Dict) -> Callable:
            app_logger = None
            log = None

            try:
                from flask import current_app
                if current_app.logger.getEffectiveLevel() > level:
                    return f(*args, **kwargs)
                app_logger = current_app.logger
            except RuntimeError:
                # If this decorator is called outside of the Flask application context,
                # you should get away right now.
                return f(*args, **kwargs)

            if level <= logging.DEBUG:
                log = app_logger.debug
            elif logging.DEBUG < level <= logging.INFO:
                log = app_logger.info
            elif logging.INFO < level <= logging.WARN:
                log = app_logger.warn
            elif logging.WARN < level <= logging.ERROR:
                log = app_logger.error
            else:
                log = app_logger.critical

            # Function arguments
            traced_func_args = []
            for k, v in inspect.getcallargs(f, *args, **kwargs).items():
                if k == 'self':
                    continue

                v = '********' if k in {'password', 'secret'} else __r.repr(v).replace('"', "'")
                traced_func_args.append('{}={}'.format(k, v))

            from flask import request

            # Get query parameters
            traced_request_args = []
            for k, v in request.args.items():
                v = '********' if k in {'password', 'secret'} else __r.repr(v).replace('"', "'")
                traced_request_args.append('{}={}'.format(k, v))

            # Post values
            traced_post_values = []
            if request.method in {'POST', 'PUT'}:
                json_args = request.json
                if json_args is not None:
                    for k, v in json_args.items():
                        v = '********' if k in {'password', 'secret'} else __r.repr(v).replace('"', "'")
                        traced_post_values.append('{}={}'.format(k, v))
                else:
                    for k, v in request.form.items():
                        v = '********' if k in {'password', 'secret'} else __r.repr(v).replace('"', "'")
                        traced_post_values.append('{}={}'.format(k, v))

            # Extra information
            trace_info_list = ['trace_pathname={}'.format(inspect.getfile(f))]
            try:
                trace_info_list.append('trace_lineno={}'.format(inspect.getsourcelines(f)[1]))
            except IndexError:
                pass

            trace_uuid = __get_trace_uuid()
            function_args = ' '.join(traced_func_args)
            query_args = ' '.join(traced_request_args)
            post_values = ' '.join(traced_post_values)
            trace_info = ' '.join(trace_info_list)
            log('trace_uuid={} method={} func_name={} func_args:{} query_args:{} post_values:{} trace_info:{}'.format(
                trace_uuid, request.method, f.__name__, function_args, query_args, post_values, trace_info))

            return f(*args, **kwargs)

        wrapper.__doc__ = f.__doc__
        wrapper.__name__ = f.__name__

        return wrapper

    return outer
