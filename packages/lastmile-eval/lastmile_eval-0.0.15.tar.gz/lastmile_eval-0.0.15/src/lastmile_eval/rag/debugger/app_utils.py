import dataclasses
from dataclasses import dataclass
from enum import Enum
import logging
import os
import subprocess
from dotenv import load_dotenv
import lastmile_utils.lib.core.api as core_utils
from pydantic import field_validator


from typing import Any, Optional


logger = logging.getLogger(__name__)
logging.basicConfig()


class ServerMode(str, Enum):
    """
    Server mode dictates how the application is run and how it communicates with
    the lastmile endpoints.

    PROD: The application is run with bundled frontend assets and hits the production
    lastmileai.dev endpoints.

    DEBUG: The application is run with the frontend server running in the background
    on port 3001 and hits the localhost:3000 lastmile endpoints.
    """

    DEBUG = "DEBUG"
    PROD = "PROD"


class LaunchConfig(core_utils.Record):
    run_llm_script_path: Optional[str] = None
    run_llm_timeout_s: int = 2
    server_port: int = 8000
    server_mode: ServerMode = ServerMode.PROD
    # TODO:
    # env_file_path: Optional[str] = None

    @field_validator("server_mode", mode="before")
    def convert_to_mode(
        cls, value: Any
    ) -> ServerMode:  # pylint: disable=no-self-argument
        if isinstance(value, str):
            try:
                return ServerMode[value.upper()]
            except KeyError as e:
                raise ValueError(f"Unexpected value for mode: {value}") from e
        return value


@dataclass
class AppState:
    server_mode: ServerMode = ServerMode.PROD
    run_llm_script_path: str | None = None
    run_llm_script_timeout_s: int = 2
    lastmile_api_token: str = ""


def load_api_token(server_mode: ServerMode):
    """
    Load the Lastmile API token from the environment.
    """
    load_dotenv()
    token_key = (
        "LASTMILE_API_TOKEN_DEV"
        if server_mode == ServerMode.DEBUG
        else "LASTMILE_API_TOKEN"
    )

    token = os.getenv(token_key)
    if token is None:
        raise ValueError(f"Missing API token: {token_key}")

    return token


def update_app_state_from_launch_config(
    launch_config: LaunchConfig, app_state: AppState
):
    app_state = dataclasses.replace(
        app_state,
        server_mode=launch_config.server_mode,
        lastmile_api_token=load_api_token(launch_config.server_mode),
        run_llm_script_path=launch_config.run_llm_script_path,
        run_llm_script_timeout_s=launch_config.run_llm_timeout_s,
    )
    return app_state


def run_frontend_server_background(client_dir: str) -> bool:
    logger.info("Running frontend server in background")
    # Yarn settles dependencies
    subprocess.Popen(["yarn"], cwd=client_dir)

    # Start the frontend server
    subprocess.Popen(
        ["yarn", "start"],
        cwd=client_dir,
        stdin=subprocess.PIPE,
    )

    return True


def get_lastmile_endpoint(api_route: str, server_mode: ServerMode):
    """
    Get the lastmile endpoint for a given route.
    """
    if server_mode == ServerMode.DEBUG:
        return f"http://localhost:3000/api/{api_route}"
    else:
        return f"https://lastmileai.dev/api/{api_route}"
