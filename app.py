from flask import Flask
import logging

app = Flask(__name__)


@app.route("/hello")
def hello():
    app.logger.debug('this is a DEBUG message')
    app.logger.info('this is an INFO message')
    app.logger.warning('this is a WARNING message')
    app.logger.error('this is an ERROR message')
    app.logger.critical('this is a CRITICAL message')
    return "Hello Gunicorn!"
