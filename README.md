# github_webhook_watcher

A simple server that watches github repository for updates and automatically
refreshes changes from a remote server.

Intended for use with either a file-watcher, but also supports running a
separate script on update.

## Installation

```sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

First, copy `config.py.template` to `config.py`, filling it out with the values
you want.

Then, in the main directory of this repository, run:

```sh
python3 server.py
```

And that's it!
