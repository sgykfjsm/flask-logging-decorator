import logging

from flask import Flask
from flask.logging import default_handler

from flask_logging_decorator import trace


app = Flask(__name__)
app.logger.setLevel(logging.WARN)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
default_handler.setFormatter(formatter)

LOG = app.logger


@app.route('/', methods=['GET', 'POST'])
@trace(logging.ERROR)
def index():
    LOG.warn('warn')
    LOG.error('error')
    LOG.info('info')
    LOG.critical('critical')
    app.logger.debug('debug')
    return 'hello'


if __name__ == '__main__':
    app.run()
