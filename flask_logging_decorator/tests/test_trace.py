from logging import NOTSET, INFO, ERROR
from typing import Any, List, Dict

from flask import Flask
import pytest
from pytest_mock import mocker

from flask_logging_decorator import trace

app = Flask(__name__)


def fake_handler() -> None:
    pass


@pytest.fixture
def values() -> Dict:
    return {'key1': 'value1'}


@pytest.fixture
def get_expected() -> List[str]:
    return ['ERROR', 'trace_uuid=', 'endpoint=/foo/bar', 'method=GET', 'func_name=fake_handler', 'func_args: ',
            "query_args:key1='value1'", 'post_values:', 'trace_info:trace_pathname=']


@pytest.fixture
def post_expected() -> List[str]:
    return ['ERROR', 'trace_uuid=', 'endpoint=/foo/bar', 'method=POST', 'func_name=fake_handler', 'func_args: ',
            'query_args: ', "post_values:key1='value1'", 'trace_info:trace_pathname=']


@pytest.fixture
def put_expected() -> List[str]:
    return ['ERROR', 'trace_uuid=', 'endpoint=/foo/bar', 'method=PUT', 'func_name=fake_handler', 'func_args: ',
            'query_args: ', "post_values:key1='value1'", 'trace_info:trace_pathname=']


@pytest.fixture
def get_expected_critical() -> List[str]:
    return ['CRITICAL', 'trace_uuid=', 'endpoint=/foo/bar', 'method=GET', 'func_name=fake_handler', 'func_args: ',
            "query_args:key1='value1'", 'post_values:', 'trace_info:trace_pathname=']


@pytest.fixture
def post_expected_critical() -> List[str]:
    return ['CRITICAL', 'trace_uuid=', 'endpoint=/foo/bar', 'method=POST', 'func_name=fake_handler', 'func_args: ',
            'query_args: ', "post_values:key1='value1'", 'trace_info:trace_pathname=']


@pytest.fixture
def put_expected_critical() -> List[str]:
    return ['CRITICAL', 'trace_uuid=', 'endpoint=/foo/bar', 'method=PUT', 'func_name=fake_handler', 'func_args: ',
            'query_args: ', "post_values:key1='value1'", 'trace_info:trace_pathname=']


@pytest.mark.parametrize(('app_log_level', 'trace_log_level'), [(ERROR, NOTSET), (ERROR, INFO), (ERROR, ERROR), (INFO, ERROR)])
@pytest.mark.parametrize(('method', 'is_json'), [('GET', False), ('POST', False), ('PUT', True)])
def test_trace(
        mocker: mocker, caplog: Any, method: str, get_expected: List[str], post_expected: List[str],
        put_expected: List[str], is_json: bool, values: Dict, app_log_level: int, trace_log_level: int) -> None:
    mock_request = mocker.patch('flask.request')

    mock_request.method = method
    mock_request.args = {}
    mock_request.form = {}
    mock_request.json = None
    mock_request.path = '/foo/bar'

    expected = get_expected
    if method == 'GET':
        mock_request.args = values
    elif method == 'POST':
        expected = post_expected
    elif method == 'PUT':
        expected = put_expected

    if method in {'POST', 'PUT'}:
        if is_json:
            mock_request.json = values
        else:
            mock_request.form = values

    app.logger.setLevel(app_log_level)
    with caplog.at_level(app_log_level):
        with app.app_context():
            outer = trace(trace_log_level)
            wrapper = outer(fake_handler)
            wrapper()

    if app_log_level == ERROR and trace_log_level == INFO:
        assert caplog.text == ''
    else:
        for exp in expected:
            assert exp in caplog.text
