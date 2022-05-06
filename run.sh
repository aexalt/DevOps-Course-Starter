#!/bin/bash
exec gunicorn --config /todo_app/gunicorn_config.py app.wsgi:app