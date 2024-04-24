import asyncio
from enum import Enum
import os
import sys
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
import requests


app = Flask(__name__, static_url_path="", static_folder="./client/build")
CORS(app, resources={r"/api/*": {"origins": "*"}})


class ServerMode(Enum):
    DEBUG = "DEBUG"
    PROD = "PROD"


# TODO: Configure via CLI
SERVER_MODE = ServerMode.PROD


load_dotenv()
LASTMILE_API_TOKEN = (
    os.getenv("LASTMILE_API_TOKEN_DEV")
    if SERVER_MODE == ServerMode.DEBUG  # type: ignore
    else os.getenv("LASTMILE_API_TOKEN")
)


def get_lastmile_endpoint(api_route: str):
    if SERVER_MODE == ServerMode.DEBUG:
        return f"http://localhost:3000/api/{api_route}"
    else:
        return f"https://lastmileai.dev/api/{api_route}"


@app.route("/")
def home():
    return app.send_static_file("index.html")


def get_request(api_route: str):
    res = requests.get(
        get_lastmile_endpoint(api_route),
        headers={"Authorization": f"Bearer {LASTMILE_API_TOKEN}"},
        timeout=30,
    )
    return res.json()


@app.get("/api/evaluation_sets/list")
def list_evaluation_sets():
    # TODO: Support query params for pagination and filtering
    return get_request("evaluation_sets/list")


@app.get("/api/evaluation_test_cases/list")
def list_evaluation_test_cases(evaluationSetId: str | None = None):
    # TODO: Support query params from pagination and filtering
    api_route = "evaluation_test_cases/list"
    if evaluationSetId:
        api_route += f"?evaluationSetId={evaluationSetId}"

    return get_request(api_route)


def run_backend_server():
    app.run(
        port=8080,
        # debug=debug,
        # use_reloader=debug,
    )


async def main_with_args(argv: list[str]) -> int:
    run_backend_server()
    return 0


def main() -> int:
    argv = sys.argv
    return asyncio.run(main_with_args(argv))


if __name__ == "__main__":
    retcode: int = main()
    sys.exit(retcode)
