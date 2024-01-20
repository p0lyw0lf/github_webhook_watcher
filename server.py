from sanic import Sanic
from sanic.request import Request
from sanic.response import text, HTTPResponse
from sanic.log import logger

app = Sanic("github_webhook_watcher")
app.update_config("./config.py")


@app.route("/")
async def index(request):
    logger.info("index")
    return text("Hello, world.")


@app.route("/webhook", methods=["POST"])
async def webhook(request: Request) -> HTTPResponse:
    github_event = request.headers["x-github-event"]

    if github_event == "push":
        payload = request.json
        commit = payload.after
        logger.info(f"Newest commit: {commit}")

    return text("Accepted", 202)
