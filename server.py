from sanic import Sanic
from sanic.request import Request
from sanic.response import text, HTTPResponse
from sanic.log import logger
import hashlib
import hmac

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


@app.route("/")
async def index(request):
    return text("Hello, world.")


@app.route("/webhook", methods=["POST"])
async def webhook(request: Request) -> HTTPResponse:
    signature = request.headers["x-hub-signature-256"]
    if not verify_signature(request.body, signature):
        return text("Invalid Signature", 403)

    github_event = request.headers["x-github-event"]
    if github_event == "push":
        payload = request.json
        repository = payload.get("repository", None)
        logger.info(f"{repository=}")

    return text("Accepted", 202)
