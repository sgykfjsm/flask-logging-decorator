import logging
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
    return {'key1': 'value1', 'key2': 'value2'}


@pytest.fixture
def get_expected() -> List[str]:
    return ['ERROR', 'trace_uuid=', 'method=GET', 'func_name=fake_handler', 'func_args: ',
            "query_args:key1='value1' key2='value2'", 'post_values:', 'trace_info:trace_pathname=']


@pytest.fixture
def post_expected() -> List[str]:
    return ['ERROR', 'trace_uuid=', 'method=POST', 'func_name=fake_handler', 'func_args: ',
            'query_args: ', "post_values:key1='value1' key2='value2'", 'trace_info:trace_pathname=']


@pytest.fixture
def put_expected() -> List[str]:
    return ['ERROR', 'trace_uuid=', 'method=PUT', 'func_name=fake_handler', 'func_args: ',
            'query_args: ', "post_values:key1='value1' key2='value2'", 'trace_info:trace_pathname=']


@pytest.mark.parametrize(('method', 'is_json'), [('GET', False), ('POST', False), ('PUT', True)])
def test_get_parameter_logging(
        mocker: mocker, caplog: Any,
        method: str, get_expected: List[str], post_expected: List[str], put_expected: List[str],
        is_json: bool, values: Dict) -> None:
    mock_request = mocker.patch('flask.request')

    mock_request.method = method
    mock_request.args = {}
    mock_request.form = {}
    mock_request.json = None

    expected = get_expected
    if method == 'GET':
        mock_request.args = values
    elif method == 'POST':
        expected = post_expected
        mock_request.form = values
    elif method == 'PUT':
        expected = put_expected

    if method in {'POST', 'PUT'} and is_json:
        mock_request.json = values

    with caplog.at_level(logging.ERROR):
        with app.app_context():
            outer = trace(logging.ERROR)
            wrapper = outer(fake_handler)
            wrapper()

    for exp in expected:
        assert exp in caplog.text
