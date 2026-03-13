#!/bin/bash

celery -A app.services.reminders worker --loglevel=info &
celery -A app.services.reminders beat --loglevel=info &
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload