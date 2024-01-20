#!/bin/env sh

source .venv/bin/activate
pip3 install --upgrade -r requirements.txt

sudo systemctl daemon-reload
sudo systemctl restart bot-github_webhook_watcher.service
