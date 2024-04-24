import logging
import os
import subprocess
from dataclasses import dataclass
from enum import Enum
from functools import partial
from typing import NewType

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.trace.span import Span
from pydantic import BaseModel
from result import Err, Ok

import lastmile_eval.rag.debugger.prompt_iteration.run_user_llm_script as lib_run_user_llm_script

app = FastAPI()

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


class EvaluationSetStatus(str, Enum):
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"


DebugTraceID = NewType("DebugTraceID", str)
EvaluationSetID = NewType("EvaluationSetID", str)
EvaluationSetResultID = NewType("EvaluationSetResultID", str)
MetricName = NewType("MetricName", str)
ParameterID = NewType("ParameterID", str)


@dataclass(frozen=True)
class DebugTrace:
    id: DebugTraceID
    spans: list[Span]


@dataclass(frozen=True)
class EvaluationSet:
    id: EvaluationSetID
    name: str
    created: int
    status: EvaluationSetStatus
    query_gt: str
    parameters: dict[ParameterID, int | float | str | bool] | None = None
    metrics: dict[MetricName, float | str] | None = None


@dataclass(frozen=True)
class EvaluationSetResult:
    id: EvaluationSetResultID
    trace_id: str
    query: str
    context: str | None = None  # TODO: Handle other trace fields
    fully_resolved_prompt: str | None = None
    response: str | None = None
    ground_truth: str | None = None
    metrics: dict[MetricName, float | str] | None = None


def _run_frontend_server_background() -> bool:
    logging.info("Running frontend server in background")
    # Yarn settles dependencies
    subprocess.Popen(["yarn"], cwd="client/.")

    # Start the frontend server
    subprocess.Popen(
        ["yarn", "start"],
        cwd="client/.",
        stdin=subprocess.PIPE,
    )

    return True


_run_frontend_server_background()


def get_lastmile_endpoint(api_route: str):
    if SERVER_MODE == ServerMode.DEBUG:
        return f"http://localhost:3000/api/{api_route}"
    else:
        return f"https://lastmileai.dev/api/{api_route}"


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


@app.get("/api/trace/read")
def get_trace(id: str | None = None):
    return get_request(f"trace/read?id={id}")


class PromptContainer(BaseModel):
    prompt: str


@app.post("/api/run_user_llm_script")
def run_user_llm_script(prompt_container: PromptContainer, response: Response):
    print("Running user LLM script")
    config = lib_run_user_llm_script.RunUserLLMScriptconfig(
        # TODO: unhardcode this stuff
        executable="../../examples/rag_debugger/run_llm.py",
        timeout_s=2,
    )

    # TODO: can make this global state
    runner = partial(lib_run_user_llm_script.run_user_llm_script, config)

    script_response = runner(prompt_container.prompt)

    match script_response:
        case Ok(response):
            return {"response": response}
        case Err(error):
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {message: error.message}
