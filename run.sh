#!/bin/bash
exec gunicorn --config gunicorn_config.py app.wsgi:todo_app