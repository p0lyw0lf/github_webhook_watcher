#!/bin/sh

source .venv/bin/activate
sanic server --host=0.0.0.0
