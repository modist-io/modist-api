#!/usr/bin/env bash

alembic upgrade head
uvicorn modist.app:app --host 0.0.0.0 --port 80
