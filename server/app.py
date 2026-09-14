#!/usr/bin/env python3
import os
from flask import Flask, request, current_app, g, make_response

app = Flask(__name__)

# TRIGGER REQUEST HOOKS
@app.before_request # runs function before each request
def app_path():
    g.path = os.path.abspath(os.getcwd())

# HTTP REQUEST
@app.route('/')
def index():
    host = request.headers.get('Host')
    appname = current_app.name          # ACCESSING APPLICATION CONTEXT
    # use Flask's make_response() function:
    response_body = f'''                
        <h1>The host for this page is {host}</h1>'
        <h2>The name of this application is {appname}</h2>   # ACCESSING APPLICATION CONTEXT
        <h3>The path of this application on the user's device is {g.path}</h3>   # TRIGGER REQUEST HOOKS
    '''
    status_code = 200   # 202 = signifies that a request has been received by the server
    headers = {}
    return make_response(response_body, status_code, headers)   # Response object
                
if __name__ == '__main__':
    app.run(port=5555, debug=True)
