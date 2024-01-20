from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class Repository:
    """
    The (relative) path of the repository you want to have updated
    """
    local: Path
    """
    The branch you want to track.
    """
    branch: str
    """
    The remote origin for this branch. Defaults to `"origin"`
    """
    remote: Optional[str]
    """
    The script to run after an update occurs
    Set to `None` to not run anything
    """
    after_update: Optional[Path]


"""
Maps repository remotes to configurations. Formatted like
`"p0lyw0lf/github_webhook_watcher"`
"""
REPOSITORIES: dict[str, Repository] = {
    "p0lyw0lf/github_webhook_watcher": Repository(Path("."), "main", None,
                                                  None)
}
"""
The secret value you share with GitHub to authenticate webhook requests
See
https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
for more information
"""
SECRET: str = b"secret"
