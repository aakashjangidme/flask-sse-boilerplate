import uuid

from flask import Flask, g


def generate_request_id():
    """Generate a unique request ID."""
    return str(uuid.uuid4())


def init_app(app: Flask):
    @app.before_request
    def before_request():
        g.request_id = generate_request_id()

    @app.after_request
    def after_request(response):
        # Attach the request ID to the response headers (optional)
        response.headers['X-Request-ID'] = g.request_id
        return response
