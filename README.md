# The Request-Response Cycle

**Status:** ✅ Completed - September 14, 2026

Web browsers cannot execute Python code. To make our views show up in the browser, Flask needs to translate HTTP requests into Python objects and new Python objects into HTTP responses. There are plenty of strategies to do this by hand, but Flask makes our lives easier with Werkzeug - Flask generates WSGI maps for the application with little to no manual configuration.

This lesson walks through the request-response cycle in Flask applications, and this repo contains the completed implementation.

## The Scenario

Build a simple request-response trigger for a newly built server: a single route that takes the host's information and displays it, along with the application name and the server-side path, with the proper status code.

## What Was Built

The `/` route in `server/app.py` now:

- Reads the incoming request's `Host` header via Flask's request context (`request.headers.get('Host')`)
- Reads the running app's name via the application context (`current_app.name`)
- Uses a `@app.before_request` hook to set `g.path` to the absolute working directory path before every request
- Builds the response body, status code, and headers explicitly, then returns them together via Flask's `make_response()` function

Final `server/app.py`:

```python
#!/usr/bin/env python3
import os
from flask import Flask, request, current_app, g, make_response

app = Flask(__name__)

@app.before_request  # runs before each request
def app_path():
    g.path = os.path.abspath(os.getcwd())

@app.route('/')
def index():
    host = request.headers.get('Host')
    appname = current_app.name
    response_body = f'''
        <h1>The host for this page is {host}</h1>
        <h2>The name of this application is {appname}</h2>
        <h3>The path of this application on the user's device is {g.path}</h3>
    '''
    status_code = 200
    headers = {}
    return make_response(response_body, status_code, headers)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
```

## How to Run It

1. Install dependencies:
   ```bash
   pipenv install
   ```
2. Activate the environment:
   ```bash
   pipenv shell
   ```
3. Run the server:
   ```bash
   cd server
   python app.py
   ```
4. Visit `http://localhost:5555` in a browser, or run `curl http://localhost:5555`. You should see the host, application name, and working directory path rendered on the page.

## Key Concepts Covered

- **Request context** → Flask generates a request context after receiving a request and before running the view, so `request` is available without being passed explicitly as an argument.
- **Application context** → `current_app` gives access to information about the running application instance.
- **`g` object** → a per-request storage object, reset with every new request; used here to hold the computed file path.
- **Request hooks** → `@app.before_request` runs a function before every view, useful for setup work that many routes share.
- **Response objects** → `make_response()` builds a response from a body, status code, and headers, which is more explicit and extensible than returning a bare string.
- **Status codes** → this route returns `200 OK`, signifying the request was received and a response was successfully generated.

## Tools & Resources

- [Flask: QuickStart](https://flask.palletsprojects.com/en/stable/quickstart)
- [API - Pallets Projects](https://flask.palletsprojects.com/en/2.2.x/api/)
- [HTTP request methods - Mozilla](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [HTTP response status codes - Mozilla](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [Response Objects - Pallets Projects](https://flask.palletsprojects.com/en/2.2.x/api/#response-objects)

## Considerations

- **Status codes:** see [Mozilla: HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status) for the full list of common codes beyond 200 (e.g. 202 Accepted, 204 No Content, 404 Not Found).
- **Redirects:** for responses that should send the browser elsewhere rather than display an HTML body, Flask's `redirect()` function is used, typically paired with a 301 (Moved Permanently) or 302 (Found) status code. It takes one argument: the URL of the relocated resource.