import os
from dataclasses import dataclass
from typing import Any, Callable, cast

import lastmile_utils.lib.core.api as core_utils
import pandas as pd
import requests
import result
from result import Err, Ok

import lastmile_eval.rag.debugger.evaluation_lib as evaluation_lib
from lastmile_eval.rag.debugger.common import core as core


@dataclass
class CreateEvaluationsResult:
    success: bool
    message: str


@dataclass
class CreateTestSetsResult:
    success: bool
    message: str
    ids: list[core.TestSetID]


def _http_get(base_url: str, endpoint: str, headers: dict[str, str]):
    return requests.get(
        os.path.join(base_url, "api", endpoint), headers=headers
    )


def _http_post_json(
    base_url: str, endpoint: str, headers: dict[str, str], data: dict[str, Any]
):
    return requests.post(
        os.path.join(base_url, "api", endpoint), headers=headers, json=data
    )


def _auth_header(lastmile_api_token: core.APIToken):
    return {
        "Authorization": f"Bearer {lastmile_api_token}",
    }


def download_test_set_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,  # "Explicit is better than implicit." - The Zen of Python
    test_set_id: core.TestSetID,
) -> core.Res[core.DFTestSet]:
    endpoint = "evaluation_test_cases/list"
    headers = _auth_header(lastmile_api_token)
    response = _http_get(base_url, endpoint, headers).json()
    print(response)
    raw_test_cases = response["evaluationTestCases"]

    def _extract_record(record: dict[str, Any]) -> dict[str, str | None]:
        return record

    df_records = pd.DataFrame.from_records(  # type: ignore
        map(_extract_record, raw_test_cases)
    )

    return core.df_as_df_test_set(
        df_records.query(f"testSetId == '{test_set_id}'")  # type: ignore
        .rename(
            columns={
                "id": "testCaseId",
            }
        )
        .reset_index()
    )


def run_evaluations_helper(
    df_test_cases: core.DFTestSet,
    trace_level_evaluators: list[core.RAGQueryTraceLevelEvaluator],
    dataset_level_evaluators: list[core.DatasetLevelEvaluator],
) -> core.Res[
    tuple[
        core.DFRAGQueryTraceEvaluations | None,
        core.DFRAGQueryDatasetEvaluations | None,
    ]
]:
    df_trace_level = None
    df_dataset_level = None

    dfs_evaluations_trace_level: list[core.DFRAGQueryTraceEvaluations] = []
    for evaluator in trace_level_evaluators:
        df_trace_level_ = evaluator(df_test_cases)
        dfs_evaluations_trace_level.append(df_trace_level_)

    if len(dfs_evaluations_trace_level) > 0:
        df_trace_level = cast(
            core.DFRAGQueryTraceEvaluations, pd.concat(dfs_evaluations_trace_level)  # type: ignore
        )

    dfs_dataset_level: list[core.DFRAGQueryDatasetEvaluations] = []
    for evaluator in dataset_level_evaluators:
        if len(df_test_cases["testSetId"].unique()) > 1:  # type: ignore
            return Err(
                ValueError(
                    "Dataset-level evaluators were given, but "
                    "multiple test sets were found. "
                    "Currently, only one test set per dataframe "
                    "is supported."
                )
            )
        df_dataset_level_ = evaluator(df_test_cases)

        dfs_dataset_level.append(df_dataset_level_)

    if len(dfs_dataset_level) > 0:
        df_dataset_level = cast(
            core.DFRAGQueryDatasetEvaluations, pd.concat(dfs_dataset_level)  # type: ignore
        )

    return Ok((df_trace_level, df_dataset_level))


def run_and_store_evaluations_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    test_set_id: core.TestSetID,
    evaluation_set_name: str,
    project_id: core.ProjectID,
    trace_level_evaluators: list[core.RAGQueryTraceLevelEvaluator],
    dataset_level_evaluators: list[core.DatasetLevelEvaluator],
) -> core.Res[CreateEvaluationsResult]:
    """Output: Success?"""

    base_url = core.BaseURL("https://lastmileai.dev")
    df_test_cases = download_test_set_helper(
        base_url,
        lastmile_api_token,
        test_set_id,
    )

    dfs_metrics = result.do(
        run_evaluations_helper(
            df_test_cases_ok,
            trace_level_evaluators,
            dataset_level_evaluators,
        )
        for df_test_cases_ok in df_test_cases
    )

    def _store_results(
        dfs_metrics: tuple[
            core.DFRAGQueryTraceEvaluations | None,
            core.DFRAGQueryDatasetEvaluations | None,
        ]
    ) -> core.Res[CreateEvaluationsResult]:
        df_metrics_trace_level, df_metrics_dataset_level = dfs_metrics

        return store_evaluation_set_results_helper(
            base_url,
            lastmile_api_token,
            evaluation_set_name,
            project_id,
            df_metrics_trace_level=df_metrics_trace_level,
            df_metrics_dataset_level=df_metrics_dataset_level,
        )

    return dfs_metrics.and_then(_store_results)


def store_evaluation_set_results_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    evaluation_set_name: str,
    project_id: core.ProjectID,
    df_metrics_trace_level: core.DFRAGQueryTraceEvaluations | None = None,
    df_metrics_dataset_level: core.DFRAGQueryDatasetEvaluations | None = None,
) -> core.Res[CreateEvaluationsResult]:
    """
    Upload evaluations results for persistence and analysis in UI.

    Metrics can be either trace-level or dataset-level.
    Both are optional, at least one is required.


    Output: Success?"""
    if df_metrics_trace_level is None and df_metrics_dataset_level is None:
        raise ValueError(
            "At least one of trace_level or dataset_level must be provided"
        )

    def _get_all_test_set_ids(
        df_metrics_trace_level: core.DFRAGQueryTraceEvaluations | None,
        df_metrics_dataset_level: core.DFRAGQueryDatasetEvaluations | None,
    ) -> set[core.TestSetID]:
        test_set_ids_trace_level = (  # type: ignore
            set(df_metrics_trace_level.testSetId.unique())  # type: ignore
            if df_metrics_trace_level is not None
            else set()
        )
        test_set_ids_dataset_level = (  # type: ignore
            set(df_metrics_dataset_level.testSetId.unique())  # type: ignore
            if df_metrics_dataset_level is not None
            else set()
        )
        return set(test_set_ids_trace_level) | set(test_set_ids_dataset_level)  # type: ignore

    all_test_set_ids = _get_all_test_set_ids(
        df_metrics_trace_level, df_metrics_dataset_level
    )

    all_results: list[CreateEvaluationsResult] = []

    for test_set_id in all_test_set_ids:
        result_for_set = _store_evaluations_for_test_set(
            base_url,
            lastmile_api_token,
            evaluation_set_name,
            test_set_id,
            project_id,
            df_metrics_trace_level,
            df_metrics_dataset_level,
        )

        all_results.append(result_for_set)

    is_success = all(result_.success for result_ in all_results)
    message = ", ".join(result_.message for result_ in all_results)
    return Ok(
        CreateEvaluationsResult(
            success=is_success,
            message=message,
        )
    )


def _store_evaluations_for_test_set(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    evaluation_set_name: str,
    test_set_id: core.TestSetID,
    project_id: core.ProjectID,
    df_metrics_trace_level: core.DFRAGQueryTraceEvaluations | None,
    df_metrics_dataset_level: core.DFRAGQueryDatasetEvaluations | None,
) -> CreateEvaluationsResult:
    endpoint = "evaluation_sets/create"
    headers = _auth_header(lastmile_api_token)

    trace_level_metrics = []
    dataset_level_metrics = []

    if df_metrics_trace_level is not None:
        df_trace = (
            df_metrics_trace_level.query(  # type: ignore[fixme]
                f"testSetId == '{test_set_id}'"
            )
            .rename(columns={"value": "metricValue"})
            .drop(
                columns=["testSetId"],
            )
        )

        trace_level_metrics = df_trace.to_dict("records")  # type: ignore[fixme]

    if df_metrics_dataset_level is not None:
        df_dataset = (
            df_metrics_dataset_level.query(  # type: ignore[fixme]
                f"testSetId == '{test_set_id}'"
            )
            .rename(columns={"value": "metricValue"})
            .drop(
                columns=["testSetId"],
            )
        )

        dataset_level_metrics = df_dataset.to_dict("records")  # type: ignore[fixme]

    data: dict[str, Any] = {
        "testSetId": test_set_id,
        "name": evaluation_set_name,
        "evaluationMetrics": trace_level_metrics,
        "evaluationSetMetrics": dataset_level_metrics,
        # "projectId": project_id,
    }
    response = _http_post_json(base_url, endpoint, headers, data)
    return CreateEvaluationsResult(
        success=response.status_code == 200,
        message=response.text,
    )


def default_dataset_aggregators(
    trace_level_evaluator: core.RAGQueryTraceLevelEvaluator,
) -> list[core.DatasetLevelEvaluator]:
    def _mean(df: core.DFTestSet) -> core.DFRAGQueryDatasetEvaluations:
        trace_evals = trace_level_evaluator(df)
        aggregated = (  # type: ignore
            trace_evals.groupby(["testSetId", "metricName"])[["value"]]  # type: ignore
            .mean()
            .reset_index()
            .drop(
                columns=[
                    "ragQueryTraceId",
                ],
                errors="ignore",
            )
        )
        renamed = aggregated.assign(  # type: ignore
            metricName=lambda df: df.metricName + "_mean"  # type: ignore
        )

        # vscode can infer more about pandas than cli pyright
        # vscode thinks cast is redundant
        # CLI needs the cast otherwise reports:
        # "Argument type is partially unknown..."
        renamed = cast(pd.DataFrame, renamed)  # type: ignore[fixme]

        return core.df_as_df_dataset_evaluations(renamed)

    return [_mean]


def user_provided_evaluators_to_all_typed_evaluators(
    trace_level_evaluators: dict[str, Callable[..., core.T_inv]],
    dataset_level_evaluators: dict[str, Callable[..., core.T_inv]],
) -> tuple[
    list[core.RAGQueryTraceLevelEvaluator], list[core.DatasetLevelEvaluator]
]:
    trace_evaluators_typed = [
        core.callable_as_trace_level_evaluator(metric_name, evaluator)
        for metric_name, evaluator in trace_level_evaluators.items()
    ]

    given_dataset_evaluators_typed = [
        core.callable_as_dataset_level_evaluator(metric_name, evaluator)
        for metric_name, evaluator in dataset_level_evaluators.items()
    ]

    trace_evaluators_for_missing_dataset_evaluators = [
        core.callable_as_trace_level_evaluator(metric_name, evaluator)
        for metric_name, evaluator in trace_level_evaluators.items()
    ]

    default_dataset_evaluators_for_missing_names = [
        evaluation_lib.default_dataset_aggregators(trace_evaluator)
        for trace_evaluator in trace_evaluators_for_missing_dataset_evaluators
    ]

    dataset_evaluators_typed = (
        given_dataset_evaluators_typed
        + core_utils.flatten_list(default_dataset_evaluators_for_missing_names)
    )
    return trace_evaluators_typed, dataset_evaluators_typed


def download_rag_query_traces_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    # TODO use this
    project_id: core.ProjectID | None,
) -> core.Res[core.DFRAGQueryTrace]:
    endpoint = "rag_query_traces/list"
    headers = _auth_header(lastmile_api_token)
    raw_response = _http_get(base_url, endpoint, headers)
    response = raw_response.json()

    return core.df_as_df_rag_query_trace(
        pd.DataFrame.from_records(response["queryTraces"]).rename(  # type: ignore[fixme]
            columns={"id": "ragQueryTraceId"}
        )
    )


def create_test_set_from_rag_query_traces_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    df_rag_query_traces: core.DFRAGQueryTrace,
    test_set_name: str,
    ground_truth: list[str] | None = None,
) -> core.Res[CreateTestSetsResult]:
    df = core.DFTestSet(df_rag_query_traces.copy())
    if ground_truth is not None:
        df["groundTruth"] = ground_truth

    endpoint = "evaluation_test_sets/create"
    headers = _auth_header(lastmile_api_token)

    allowed_columns = [
        c
        for c in [
            "query",
            "context",
            "fullyResolvedPrompt",
            "output",
            "groundTruth",
            "ragQueryTraceId",
        ]
        if c in df.columns
    ]

    data = {  # type: ignore[fixme]
        "name": test_set_name,
        "testCases": df[allowed_columns].to_dict("records"),  # type: ignore
    }
    response = _http_post_json(base_url, endpoint, headers, data)  # type: ignore[fixme]
    response_json = response.json()
    ids = [core.TestSetID(response_json["id"])]
    return Ok(
        CreateTestSetsResult(
            success=response.status_code == 200, message=response.text, ids=ids
        )
    )


# This evaluation on entire test dataframe may be useful in some cases,
# but it's good to provide a wrapper to allow for evaluation at the
# trace-level (each row of test set)
# TODO: Have proper typing for row_func result when defining lambdas
def wrap_entire_dataframe_with_row_func_lambda(
    row_level_func: Callable[pd.Series, Any]
) -> Callable[[pd.DataFrame], list[Any]]:
    return lambda an_entire_df: _iterate_results_over_a_dataframe(
        an_entire_df, row_level_func
    )


def _iterate_results_over_a_dataframe(
    an_entire_df: pd.DataFrame, row_func: Callable[pd.Series, Any]
) -> list[Any]:
    row_result: list[Any] = []
    for _index, row in an_entire_df.iterrows():
        row_result.append(row_func(row))
    return row_result
