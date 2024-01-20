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
    The branch name you want to track
    """
    branch: str
    """
    The script to run after an update occurs
    Set to `None` to not run anything
    """
    after_update: Optional[Path]


"""
Maps repository remotes to configurations
TODO: what's the format for the `repository` in the webhook? to be seen.
"""
REPOSITORIES: dict[str, Repository] = {}
"""
The secret value you share with GitHub to authenticate webhook requests
See
https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
for more information
"""
SECRET: str = b"secret"
