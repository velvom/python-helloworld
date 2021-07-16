from flask import Flask
from flask import json
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

@app.before_first_request
def config_logging():
    '''
    #hdlr = [RotatingFileHandler('app.log', maxBytes=10000000, backupCount=5)]
    #fmt = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    #logging.basicConfig(handlers=hdlr, level=logging.DEBUG, format=fmt, datefmt='%Y-%m-%dT%H:%M:%S')
    '''
    # Remove StreamHandler to not log anything to console
    app.logger.handlers.pop(0)
    
    # Set the handler for logging to a file
    # All application related messages will be sent to the file
    apphdlr = RotatingFileHandler('app.log', maxBytes=10000000, backupCount=5)
    appformatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(endpt)s %(message)s")
    apphdlr.setFormatter(appformatter)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(apphdlr)

    # werkzeug normally sends messages to the root logger. 
    # Create a new handler to redirect the messages to the file.
    wsgihdlr = RotatingFileHandler('app.log', maxBytes=10000000, backupCount=5)
    wsgi_logger = logging.getLogger('werkzeug')
    #wsgiformatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")
    #wsgihdlr.setFormatter(wsgiformatter)
    wsgi_logger.setLevel(logging.DEBUG)
    wsgi_logger.addHandler(wsgihdlr)
    #wsgi_logger.disabled = True
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'

@app.route('/status')
def status():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )

    d = {'endpt': '/status'}
    app.logger.info('endpoint was reached', extra=d)
    return response

@app.route('/metrics')
def metrics():
    response = app.response_class(
            response=json.dumps({"status":"success","code":0,"data":{"UserCount":140,"UserCountActive":23}}),
            status=200,
            mimetype='application/json'
    )

    d = {'endpt': '/metrics'}
    app.logger.info('endpoint was reached', extra=d)
    return response

@app.route("/")
def hello():
    d = {'endpt': '/'}
    app.logger.info('endpoint was reached', extra=d)
    return "Hello World!"


if __name__ == "__main__":
    config_logging()
    d = {'endpt': 'main'}
    app.logger.info('Starting app', extra=d)
    app.run(host='0.0.0.0')
   
   