from sanic import Sanic
from sanic.request import Request
from sanic.response import text, HTTPResponse
from sanic.log import logger

import hashlib
import hmac
from typing import Optional
import asyncio

app = Sanic("github_webhook_watcher")
app.update_config("./config.py")


def verify_signature(body: bytes, signature: str) -> bool:
    if not signature:
        return False
    hash_object = hmac.new(app.config.SECRET,
                           msg=body,
                           digestmod=hashlib.sha256)
    expected_signature = f"sha256={hash_object.hexdigest()}"

    return hmac.compare_digest(expected_signature, signature)


def o_get(m: Optional[dict[str, object]], s: str) -> Optional[object]:
    # I can't believe I'm having to implement this monad LOL
    if m is None:
        return None

    return m.get(s, None)


@app.route("/")
async def index(request):
    return text("Hello, world.")


@app.route("/webhook", methods=["POST"])
async def webhook(request: Request) -> HTTPResponse:
    signature = request.headers["x-hub-signature-256"]
    if not verify_signature(request.body, signature):
        return text("Invalid Signature", 403)

    # This dance is needed to not discard the task from garbage collection
    background_task = set()
    task = asyncio.create_task(handle_webhook(request))
    background_task.add(task)
    task.add_done_callback(background_task.discard)

    return text("Accepted", 202)


LOCKS = {key: asyncio.Lock() for key in app.config.REPOSITORIES.keys()}


async def handle_webhook(request: Request):
    github_event = request.headers["x-github-event"]
    if github_event != "push":
        # Nothing to do: not a push
        return

    payload = request.json
    repository_name = o_get(o_get(payload, "repository"), "full_name")
    config = app.config.REPOSITORIES.get(repository_name, None)
    if config is None:
        logger.warn(
            f"Got webhook for repository {repository_name}, but not "
            "configured for it! Probably meant to update ./config.py"
        )
        # Nothing to do: not configured
        return

    logger.info(f"{config=}")

    ref = o_get(payload, "ref")
    if ref != f"refs/heads/{config.ref}":
        # Nothing to do: wrong ref
        return

    # Only do one update at a time
    async with LOCKS[repository_name]:
        pull_proc = await asyncio.create_subprocess_exec(
            "git",
            "pull",
            "--ff-only",
            config.remote or "origin",
            config.branch,
            cwd=config.local,
            # Pass through stdout and stderr
            stdout=None,
            stderr=None,
        )
        exit_code = await pull_proc.wait()
        if exit_code != 0:
            logger.warn(
                f"Pull for {repository_name} exited with code {exit_code}, "
                "you might want to take a look at that!"
            )
            return

        # TODO: after_update
