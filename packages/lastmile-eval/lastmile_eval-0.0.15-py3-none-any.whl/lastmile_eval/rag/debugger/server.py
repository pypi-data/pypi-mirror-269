import dataclasses
import json
import logging
import uvicorn

from lastmile_eval.rag.debugger.app import CLIENT_DIR
from lastmile_eval.rag.debugger.app_utils import run_frontend_server_background
from lastmile_eval.rag.debugger.app_utils import (
    AppState,
    LaunchConfig,
    ServerMode,
    update_app_state_from_launch_config,
)

logger = logging.getLogger(__name__)
logging.basicConfig()


def serve(launch_config: LaunchConfig):
    should_reload = launch_config.server_mode != "PROD"
    app_state = update_app_state_from_launch_config(launch_config, AppState())
    print(f"{app_state.lastmile_api_token=}")

    # TODO: un-jank this (do it in memory)
    with open("initial_app_state.json", "w") as f:
        f.write(json.dumps(dataclasses.asdict(app_state), indent=2))

    if launch_config.server_mode == ServerMode.DEBUG:
        run_frontend_server_background(CLIENT_DIR)

    uvicorn.run(
        "lastmile_eval.rag.debugger.app:app",
        port=launch_config.server_port,
        log_level=logger.level,
        reload=should_reload,
    )
