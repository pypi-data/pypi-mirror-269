from typing import Callable, Sequence

import pandas as pd
import result

import lastmile_eval.rag.debugger.evaluation_lib as evaluation_lib
from lastmile_eval.rag.debugger.common import core as core

from typing import Any, Optional
import requests
from requests import Response


def _token(lastmile_api_token: str | None) -> core.APIToken:
    return (
        core.APIToken(lastmile_api_token)
        if lastmile_api_token is not None
        else core.APIToken(core.api_token_from_dot_env("LASTMILE_API_TOKEN"))
    )


def download_rag_query_traces(
    lastmile_api_token: str | None = None,
    project_id: str | None = None,
) -> core.DFRAGQueryTrace:
    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)
    return evaluation_lib.download_rag_query_traces_helper(
        core.BaseURL(base_url),
        core.APIToken(lastmile_api_token),
        core.ProjectID(project_id) if project_id is not None else None,
    ).unwrap_or_raise(ValueError)


def create_test_set_from_rag_query_traces(
    df_rag_query_traces: pd.DataFrame,
    test_set_name: str,
    ground_truth: list[str] | None = None,
    lastmile_api_token: str | None = None,
) -> evaluation_lib.CreateTestSetsResult:
    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)
    return result.do(
        evaluation_lib.create_test_set_from_rag_query_traces_helper(
            core.BaseURL(base_url),
            lastmile_api_token,
            df_rag_query_trace_ok,
            test_set_name,
            ground_truth,
        )
        for df_rag_query_trace_ok in core.df_as_df_rag_query_trace(
            df_rag_query_traces
        )
    ).unwrap_or_raise(ValueError)


def download_test_set(
    test_set_id: str,
    lastmile_api_token: str | None = None,
) -> pd.DataFrame:
    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)

    return evaluation_lib.download_test_set_helper(
        core.BaseURL(base_url),
        core.APIToken(lastmile_api_token),
        core.TestSetID(test_set_id),
    ).unwrap_or_raise(ValueError)


def list_test_sets(
    take: int = 10,
    lastmile_api_token: Optional[str] = None,
    # TODO: Create macro for default timeout value
    timeout: int = 60,
) -> dict[str, Any]:  # TODO: Define eplicit typing for JSON response return
    """
    Get a list of test sets from the LastMile API.

    Args:
        take: The number of test sets to return. The default is 10.
        lastmile_api_token: The API token for the LastMile API. If not provided,
            will try to get the token from the LASTMILE_API_TOKEN
            environment variable.
            You can create a token from the "API Tokens" section from this website:
            https://lastmileai.dev/settings?page=tokens
        timeout: The maximum time in seconds to wait for the request to complete.
            The default is 60.

    Returns:
        A dictionary containing the test sets.
    """
    lastmile_api_token = _token(lastmile_api_token)
    lastmile_endpoint = f"https://lastmileai.dev/api/evaluation_test_sets/list?pageSize={str(take)}"

    response: Response = requests.get(
        lastmile_endpoint,
        headers={"Authorization": f"Bearer {lastmile_api_token}"},
        timeout=timeout,
    )
    # TODO: Handle response errors
    return response.json()


def get_latest_test_set_id(
    lastmile_api_token: Optional[str] = None,
) -> str:
    """
    Convenience function to get the latest test set id. You can pass this id
    into these methods to build your offline evaluator data:
        - download_test_set
        - run_and_store_evaluations

    @param lastmile_api_token Optional(str): Used for authentication. If not
        defined, will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return str: The test set id corresponding to latest test set
    """
    test_sets: dict[str, Any] = list_test_sets(
        take=1, lastmile_api_token=lastmile_api_token
    )
    # TODO: Handle errors
    test_set_id: str = test_sets["evaluationTestSets"][0]["id"]
    return test_set_id


def run_and_store_evaluations(
    test_set_id: str,
    project_id: str,
    trace_level_evaluators: dict[
        str, Callable[[pd.DataFrame], Sequence[float]]
    ],
    dataset_level_evaluators: dict[
        str, Callable[[pd.DataFrame], Sequence[float]]
    ],
    lastmile_api_token: str | None = None,
    evaluation_set_name: str | None = None,
) -> evaluation_lib.CreateEvaluationsResult:
    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)

    (
        trace_evaluators_typed,
        dataset_evaluators_typed,
    ) = evaluation_lib.user_provided_evaluators_to_all_typed_evaluators(
        trace_level_evaluators,  # type: ignore[deliberate ignore]
        dataset_level_evaluators,  # type: ignore[deliberate ignore]
    )

    return evaluation_lib.run_and_store_evaluations_helper(
        core.BaseURL(base_url),
        core.APIToken(lastmile_api_token),
        core.TestSetID(test_set_id),
        evaluation_set_name or "Evaluation Set",
        core.ProjectID(project_id),
        trace_evaluators_typed,
        dataset_evaluators_typed,
    ).unwrap_or_raise(ValueError)


def run_evaluations(
    df_test_set: pd.DataFrame,
    trace_level_evaluators: dict[
        str, Callable[[pd.DataFrame], Sequence[float]]
    ],
    dataset_level_evaluators: dict[
        str, Callable[[pd.DataFrame], Sequence[float]]
    ],
) -> tuple[pd.DataFrame | None, pd.DataFrame | None]:
    """
    In: test set (everything needed to directly run evaluators)
    evaluators: two mappings from name to function.
    Each function should calculate a metric, i.e. return a batch of floats.

    The first mapping is trace-level, i.e. row-by-row.
    The second mapping should aggregate over traces, grouping by test set.

    NOTE: For every trace-level metric, if you do not provide the corresponding
    dataset-level metric, we will fill in defaults.

    Out: (trace-level evaluations, dataset-level evaluations)"""
    (
        trace_evaluators_typed,
        dataset_evaluators_typed,
    ) = evaluation_lib.user_provided_evaluators_to_all_typed_evaluators(
        trace_level_evaluators,  # type: ignore[deliberate ignore]
        dataset_level_evaluators,  # type: ignore[deliberate ignore]
    )

    df_test_set_typed = core.df_as_df_test_set(df_test_set)

    return result.do(
        evaluation_lib.run_evaluations_helper(
            df_test_set_ok,
            trace_evaluators_typed,
            dataset_evaluators_typed,
        )
        for df_test_set_ok in df_test_set_typed
    ).unwrap_or_raise(ValueError)


def store_evaluation_set_results(
    project_id: str,
    df_metrics_trace_level: pd.DataFrame | None = None,
    df_metrics_dataset_level: pd.DataFrame | None = None,
    lastmile_api_token: str | None = None,
    evaluation_set_name: str | None = None,
) -> evaluation_lib.CreateEvaluationsResult:
    base_url = core.BaseURL("https://lastmileai.dev")
    lastmile_api_token = _token(lastmile_api_token)

    return evaluation_lib.store_evaluation_set_results_helper(
        base_url,
        core.APIToken(lastmile_api_token),
        df_metrics_trace_level=(
            core.DFRAGQueryTraceEvaluations(df_metrics_trace_level)
            if df_metrics_trace_level is not None
            else None
        ),
        df_metrics_dataset_level=(
            core.DFRAGQueryDatasetEvaluations(df_metrics_dataset_level)
            if df_metrics_dataset_level is not None
            else None
        ),
        evaluation_set_name=evaluation_set_name or "Evaluation Set",
        project_id=core.ProjectID(project_id),
    ).unwrap_or_raise(ValueError)
