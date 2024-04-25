import json
import logging
import os
from urllib.parse import urlencode

import requests
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from result import Err, Ok

from lastmile_eval.rag.debugger.app_utils import (
    AppState,
    ServerMode,
    get_lastmile_endpoint,
)
import lastmile_eval.rag.debugger.prompt_iteration.run_user_llm_script as lib_run_user_llm_script

logger = logging.getLogger(__name__)
logging.basicConfig()


def read_global_app_state():
    try:
        # TODO: un-jank this (do it in memory)
        with open("initial_app_state.json", "r") as f:
            contents = f.read()
            # print(f"Contents: {contents}")
            loaded = json.loads(contents)
            # print(f"Loaded: {loaded}")
            app_state = AppState(**loaded)
            # print(
            #     f"Loaded initial app state: {app_state.run_llm_script_path=}"
            # )
            return app_state
    except Exception as e:
        logger.error(f"Failed to load initial app state: {e}")

        return AppState()


app_state = read_global_app_state()

app = FastAPI()

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_DIR = os.path.join(THIS_DIR, "client")
BUILD_DIR = os.path.join(CLIENT_DIR, "build")
STATIC_DIR = os.path.join(BUILD_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=BUILD_DIR)


origins = [
    "http://localhost:3001",  # dev client
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_request(api_route: str, server_mode: ServerMode):
    """
    Make a GET request to the lastmile API for given route.
    """

    global app_state
    res = requests.get(
        get_lastmile_endpoint(api_route, server_mode),
        headers={"Authorization": f"Bearer {app_state.lastmile_api_token}"},
        timeout=30,
    )
    return res.json()


@app.get("/api/evaluation_sets/list")
def list_evaluation_sets(
    search: str | None = None,
    pageSize: int | None = None,
    cursor: str | None = None,
):
    """
    List evaluation sets.
    """
    params = {
        "search": search,
        "pageSize": pageSize,
        "cursor": cursor,
    }
    params = {key: value for key, value in params.items() if value is not None}
    encoded_params = urlencode(params)
    api_route = f"evaluation_sets/list?{encoded_params}"

    global app_state
    return get_request(api_route, app_state.server_mode)


@app.get("/api/evaluation_test_cases/list")
def list_evaluation_test_cases(
    evaluationSetId: str | None = None,
    search: str | None = None,
    pageSize: int | None = None,
    cursor: str | None = None,
):
    """
    List evaluation test cases.
    """
    params = {
        "evaluationSetId": evaluationSetId,
        "search": search,
        "pageSize": pageSize,
        "cursor": cursor,
    }
    params = {key: value for key, value in params.items() if value is not None}
    encoded_params = urlencode(params)
    api_route = f"evaluation_test_cases/list?{encoded_params}"

    return get_request(api_route, app_state.server_mode)


@app.get("/api/rag_ingestion_traces/list")
def list_rag_ingestion_traces(
    search: str | None = None,
    pageSize: int | None = None,
    cursor: str | None = None,
):
    """
    List RAG ingestion traces.
    """
    params = {
        "search": search,
        "pageSize": pageSize,
        "cursor": cursor,
    }
    params = {key: value for key, value in params.items() if value is not None}
    encoded_params = urlencode(params)
    api_route = f"rag_ingestion_traces/list?{encoded_params}"

    return get_request(api_route, app_state.server_mode)


@app.get("/api/rag_query_traces/list")
def list_rag_query_traces(
    search: str | None = None,
    pageSize: int | None = None,
    cursor: str | None = None,
):
    """
    List RAG query traces.
    """
    params = {
        "search": search,
        "pageSize": pageSize,
        "cursor": cursor,
    }
    params = {key: value for key, value in params.items() if value is not None}
    encoded_params = urlencode(params)
    api_route = f"rag_query_traces/list?{encoded_params}"

    return get_request(api_route, app_state.server_mode)


@app.get("/api/trace/read")
def get_trace(id: str | None = None):
    """
    Get an OTEL trace by ID.
    """
    return get_request(f"trace/read?id={id}", app_state.server_mode)


class PromptContainer(BaseModel):
    prompt: str


@app.post("/api/run_user_llm_script")
def run_user_llm_script(prompt_container: PromptContainer, response: Response):  # type: ignore[fixme]
    """
    Run the user LLM script.
    """

    global app_state

    script_path = app_state.run_llm_script_path
    logger.debug(f"Script path: {script_path}")
    if script_path is None:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "No script path configured. Please rerun app with --help."
        }

    logger.info("Running user LLM script")
    config = lib_run_user_llm_script.RunUserLLMScriptconfig(
        executable=script_path,
        timeout_s=app_state.run_llm_script_timeout_s,
    )

    script_response = lib_run_user_llm_script.run_user_llm_script(
        config, prompt_container.prompt
    )

    match script_response:
        case Ok(response_):
            return {"response": response_}
        case Err(error):
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"message": error}


# Defines a route handler for `/*` essentially.
# NOTE: this needs to be the last route defined b/c it's a catch all route
@app.get("/{rest_of_path:path}")
async def react_app(req: Request):
    """
    Serve the frontend react app (DEBUG ONLY).
    """
    if app_state.server_mode == ServerMode.DEBUG:  # type: ignore
        return {
            "message": "Not serving bundle in DEBUG mode, use yarn start in client/"
        }
    return templates.TemplateResponse("index.html", {"request": req})
