#!/bin/env sh

. .venv/bin/activate
pip3 install --upgrade -r requirements.txt

sudo -n systemctl daemon-reload
sudo -n systemctl restart bot-github_webhook_watcher.service
