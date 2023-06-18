import logging
from pathlib import Path

from flask import has_request_context, request


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.path = request.full_path
            record.remote_addr = request.remote_addr
        else:
            record.path = None
            record.remote_addr = None

        return super().format(record)


def configure_logging(app):
    Path('logs').mkdir(exist_ok=True)
    fmt = RequestFormatter(
        '[%(asctime)s] [%(remote_addr)s] %(path)s\n -- %(message)s'
    )
    error_handler = logging.FileHandler('logs/error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(fmt)

    app.logger.addHandler(error_handler)
