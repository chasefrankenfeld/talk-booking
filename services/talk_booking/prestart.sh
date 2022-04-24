#! /usr/bin/env bash

# Let the DB start
python ./web_app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
# python ./app/initial_data.py
