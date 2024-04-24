"""
Internal interface to retrieve structured (tabular) trace data
"""

from dataclasses import dataclass
from typing import Collection

from lastmile_eval.rag.debugger.common import core as core
from lastmile_eval.rag.debugger.common import (
    query_trace_types as query_trace_types,
)

# Linear records derived from traces

# This means a pre-defined list of specific events in a predefined order
# which are completely derivable from a trace.


@dataclass(frozen=True)
class IndexingTraceLinearRecord:
    trace_id: core.IndexingTraceID
    # TODO ...


@dataclass(frozen=True)
class QueryTraceLinearRecord:
    trace_id: core.RAGQueryTraceID
    query: query_trace_types.QueryReceived
    context: query_trace_types.ContextRetrieved
    fully_resolved_prompt: query_trace_types.PromptResolved
    llm_output: query_trace_types.LLMOutputReceived
    # TODO
    # parametrized_prompt: ... = None
    # prompt_data_to_interpolate: ... = None


def get_rag_trace_linear_records(
    trace_ids: Collection[core.RAGQueryTraceID],
) -> dict[core.RAGQueryTraceID, QueryTraceLinearRecord]:
    """
    Get predefined tabular trace
        (as opposed to user-defined arbitrary tree-structure)

        Read from the trace store,
        parse & transform into the output format.
    """
    raise NotImplementedError("Not implemented yet")
