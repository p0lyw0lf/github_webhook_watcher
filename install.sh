#!/bin/env sh

dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
sudo ln -s "$dir/bot-github_webhook_watcher.service" /etc/systemd/system/bot-github_webhook_watcher.service
sudo useradd -m -U bot-github_webhook_watcher -G ubuntu
