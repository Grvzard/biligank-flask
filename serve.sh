#! /usr/bin/env sh
set -e

exec gunicorn -w 2 -k gevent --bind 0.0.0.0:7771 biligank_flask:app
