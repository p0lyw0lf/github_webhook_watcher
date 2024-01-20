from pathlib import Path


# The (relative) path of the repository you want to have updated
REPOSITORY_LOCAL = Path(".")

# The URL of the github repository you want
# TODO: what's the format for the `repository` in the webhook? to be seen.
REPOSITORY_REMOTE = "https://github.com/p0lyw0lf/github_webhook_watcher.git"

# The script to run after an update occurs
# Set to `None` to not run anything
AFTER_UPDATE = None
