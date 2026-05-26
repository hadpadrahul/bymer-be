"""Gunicorn config for VPS or Docker (see docs/DEPLOYMENT.md)."""

import multiprocessing
import os

bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")
workers = int(os.environ.get("GUNICORN_WORKERS", max(2, multiprocessing.cpu_count() * 2 + 1)))
threads = int(os.environ.get("GUNICORN_THREADS", 1))
timeout = int(os.environ.get("GUNICORN_TIMEOUT", 120))
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")
wsgi_app = "config.wsgi:application"
