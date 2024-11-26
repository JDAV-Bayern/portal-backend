#!/bin/sh

python -m manage migrate
python -m manage compilemessages

exec "$@"
