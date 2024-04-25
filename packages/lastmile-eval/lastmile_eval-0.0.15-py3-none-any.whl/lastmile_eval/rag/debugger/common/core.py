import collections.abc
import logging
import os
import traceback as tb
from typing import Callable, Literal, NewType, Protocol, Sequence, TypeVar

import dotenv
import numpy as np
import pandas as pd
from result import Err, Ok, Result

# Trace Data
TraceID = NewType("TraceID", str)


IndexingTraceID = NewType("IndexingTraceID", str)
ParamInfoKey = NewType("ParamInfoKey", str)
RagQueryEventName = Literal[
    "QueryReceived",
    "ContextRetrieved",
    "PromptResolved",
    "LLMOutputReceived",
]
RAGQueryTraceID = NewType("RAGQueryTraceID", str)
RAGTraceType = Literal["Ingestion", "Query"]

TestSetID = NewType("TestSetID", str)
MetricName = NewType("MetricName", str)

ProjectID = NewType("ProjectID", str)
APIToken = NewType("APIToken", str)
BaseURL = NewType("BaseURL", str)

# specialized container types
DFRAGQueryTrace = NewType("DFRAGQueryTrace", pd.DataFrame)

T_inv = NewType("T_inv", object)

T_cov = TypeVar("T_cov", covariant=True)

Res = Result[T_cov, Exception]

"""

DFRAGQueryTrace must have
    
    | ragQueryTraceId |  query (?) | context (?) | fullyResolvedPrompt (?) | output  (?) | indexingTraceId (?) |

    
DFTestSet must have:

    | testSetId  | testCaseId | query (?) | context (?) | fullyResolvedPrompt (?) | output (?)| ragQueryTraceId (?) |

DFRAGQueryTraceEvaluations must have
    
    | testSetId | testCaseid | metricName | value | ragQueryTraceId (?) |

DFRAGQueryDatasetEvaluations must have
        
    | testSetId | metricName | value |

"""

DFTestSet = NewType("DFTestSet", pd.DataFrame)
DFRAGQueryTraceEvaluations = NewType(
    "DFRAGQueryTraceEvaluations", pd.DataFrame
)
DFRAGQueryDatasetEvaluations = NewType(
    "DFRAGQueryDatasetEvaluations", pd.DataFrame
)


logger = logging.getLogger(__name__)

# TODO: unhardcode level and format
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s")


class RAGQueryTraceLevelEvaluator(Protocol):
    def __call__(self, df: DFTestSet) -> DFRAGQueryTraceEvaluations:
        ...


class DatasetLevelEvaluator(Protocol):
    def __call__(self, df: DFTestSet) -> DFRAGQueryDatasetEvaluations:
        ...


def _exception_info(e: Exception) -> str:
    traceback = tb.format_exception(e)
    return "".join(traceback)


def df_as_df_rag_query_trace(df: pd.DataFrame) -> Res[DFRAGQueryTrace]:
    if "ragQueryTraceId" not in df.columns:
        return Err(
            ValueError("DataFrame must have a 'ragQueryTraceId' column")
        )

    if not df.set_index("ragQueryTraceId").index.is_unique:  # type: ignore
        return Err(ValueError("ragQueryTraceId must be a key column"))
    return Ok(DFRAGQueryTrace(df))


def df_as_df_test_set(df: pd.DataFrame) -> Res[DFTestSet]:
    if "testSetId" not in df.columns:
        return Err(ValueError("DataFrame must have a 'testSetId' column"))

    if not df.set_index("testCaseId").index.is_unique:  # type: ignore
        return Err(ValueError("'testSetId' must be a key column"))
    return Ok(DFTestSet(df))


def df_as_df_trace_evaluations(df: pd.DataFrame) -> DFRAGQueryTraceEvaluations:
    if any(
        col not in df.columns
        for col in ["testSetId", "testCaseId", "metricName", "value"]
    ):
        raise ValueError(
            "DataFrame must have 'testSetId', 'traceId', 'metricName', and 'value' columns"
        )
    if not df.set_index(["testSetId", "testCaseId", "metricName"]).index.is_unique:  # type: ignore[fixme]
        raise ValueError(
            "DataFrame must have a composite key ('testSetId', 'traceId', 'metricName')"
        )
    return DFRAGQueryTraceEvaluations(df)


def df_as_df_dataset_evaluations(
    df: pd.DataFrame,
) -> DFRAGQueryDatasetEvaluations:
    if any(
        col not in df.columns for col in ["testSetId", "metricName", "value"]
    ):
        raise ValueError(
            "Dataset evaluations must have 'testSetId', 'metricName', and 'value' columns"
        )

    if any(col in df.columns for col in ["testCaseId"]):
        raise ValueError("DataFrame must not have 'testCaseId' column")

    if not df.set_index(["testSetId", "metricName"]).index.is_unique:  # type: ignore[fixme]
        raise ValueError(
            "DataFrame must have a composite key ('testSetId', 'metricName')"
        )
    return DFRAGQueryDatasetEvaluations(df)


def api_token_from_dot_env(key: str) -> str:
    dotenv.load_dotenv()
    value = os.getenv(key)
    if value is None:
        raise ValueError(
            f"Environment variable '{key}' not found. Check your .env file."
        )

    return value


def _coerce_list_like(data: T_inv) -> Result[list[float], str]:  # type: ignore[fixme]
    # TODO do this function better
    # ignoring T_inv error deliberately; see safe_run_function_as_trace_evaluator()
    # for more info.
    if isinstance(data, collections.abc.Sequence):
        if all(isinstance(x, (int, float)) for x in data):  # type: ignore
            return Ok(list(data))  # type: ignore
    elif isinstance(data, pd.Series):
        if data.dtype in [int, float]:  # type: ignore
            return Ok(data.tolist())  # type: ignore

    return Err("Data must be list-like")


def safe_run_function_as_trace_evaluator(
    # This is really not supposed to be parametric, it's supposed to be a Sequence[float].
    # Using T to make pyright warn us that the user might return something wrong.
    f: Callable[..., T_inv],
    df: DFTestSet,
) -> Sequence[float]:
    # TODO: timeout, parallelize
    N = len(df)
    try:
        out = f(df)
        match _coerce_list_like(out):
            case Ok(values):
                return values
            case Err(e):
                logger.error(
                    f"Error running trace-level evaluator: {out}, {e}"
                )
                return [np.nan] * N

    except Exception as e:
        logger.error(
            f"Error running trace-level evaluator: {_exception_info(e)}"
        )
        return [np.nan] * N


def safe_run_function_as_dataset_evaluator(
    # This is really not supposed to be parametric, it's supposed to be a Sequence[float].
    # Using T to make pyright warn us that the user might return something wrong.
    f: Callable[..., T_inv],
    df: DFTestSet,
) -> Sequence[float]:
    # TODO: timeout, parallelize
    N = len(df)
    try:
        out = f(df)
        match _coerce_list_like(out):
            case Ok(values):
                return values
            case Err(e):
                logger.error(
                    f"Error running dataset-level evaluator: {out}, {e}"
                )
                return [np.nan] * N

        return list(out)  # type: ignore[fixme]
    except Exception as e:
        logger.error(
            f"Error running dataset-level evaluator: {_exception_info(e)}"
        )
        return [np.nan] * N


def callable_as_trace_level_evaluator(
    metric_name: str, f: Callable[..., T_inv]
) -> RAGQueryTraceLevelEvaluator:
    def _wrap(df: DFTestSet) -> DFRAGQueryTraceEvaluations:
        values = safe_run_function_as_trace_evaluator(f, df)
        N = len(values)
        df_out = pd.DataFrame(
            {
                "testSetId": df["testSetId"],
                "testCaseId": df["testCaseId"],
                "metricName": [metric_name] * N,
                "value": values,
            }
        )
        return df_as_df_trace_evaluations(df_out)

    return _wrap


def callable_as_dataset_level_evaluator(
    metric_name: str, f: Callable[..., T_inv]
) -> DatasetLevelEvaluator:
    def _wrap(df: DFTestSet) -> DFRAGQueryDatasetEvaluations:
        values = safe_run_function_as_dataset_evaluator(f, df)

        # Currently, we stipulate that len(values) == 1,
        # i.e. only one testSetId can be evaluated at a time.
        test_set_ids = set(df["testSetId"].unique())  # type: ignore
        if len(values) > 1 or len(test_set_ids) > 1:  # type: ignore
            raise ValueError(
                "Dataset-level evaluators must return a single value per testSetId. "
                "Currently, only one test set can be evaluated at a time."
            )

        return df_as_df_dataset_evaluations(
            pd.DataFrame(
                {
                    "testSetId": list(test_set_ids),
                    "metricName": [metric_name],
                    "value": values,
                }
            )
        )

    return _wrap
