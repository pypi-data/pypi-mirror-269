import abc
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterator, Optional, Sequence

from opentelemetry import context as context_api
from opentelemetry import trace as trace_api
from opentelemetry.trace.span import Span
from opentelemetry.util import types

from ..common import query_trace_types

# Public API for logging


RAGQueryEvent = (
    query_trace_types.QueryReceived
    | query_trace_types.ContextRetrieved
    | query_trace_types.PromptResolved
    | query_trace_types.LLMOutputReceived
)

# TODO: Define later what the injestion_trace_types should be
RAGIngestionEvent = str | list[str]


@dataclass(frozen=True)
class RAGTraceEventResult:
    """
    Return type from marking a RAGQueryEvent or RAGIngestionEvent in a trace
    """

    is_success: bool
    message: str


class LastMileTracer(abc.ABC):
    """
    A tracer proxy around OpenTelemetry tracer. It has 3 main functionalities:

    1. Create span data and attach it to the tracer. This is the same API as
        OpenTelemetry's tracer:
            a. `start_as_current_span()`
            b. `start_span()`
    2. Mark RAG events and store their states (see `RAGQueryEvent` and
        `RAGIngestionEvent`) alongside the trace data. The methods for this are:
            a. `mark_rag_ingestion_trace_event`
            b. `mark_rag_query_trace_event`
    3. Register a dictionary of parameters to be logged and associated with
        the trace data. The methods for this are:
            a. `register_param()`
            b. `get_params()`
    """

    @abc.abstractmethod
    @contextmanager
    def start_as_current_span(  # pylint: disable=too-many-locals
        self,
        name: str,
        context: Optional[context_api.Context] = None,
        kind: trace_api.SpanKind = trace_api.SpanKind.INTERNAL,
        attributes: types.Attributes = None,
        links: Optional[Sequence[trace_api.Link]] = None,
        start_time: Optional[int] = None,
        record_exception: bool = True,
        set_status_on_exception: bool = True,
        end_on_exit: bool = True,
    ) -> Iterator[Span]:
        """
        Same API as opentelemetry.trace.Tracer.start_as_current_span
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def start_span(
        self,
        name: str,
        context: Optional[context_api.Context] = None,
        kind: trace_api.SpanKind = trace_api.SpanKind.INTERNAL,
        attributes: types.Attributes = None,
        links: Sequence[trace_api.Link] = (),
        start_time: Optional[int] = None,
        record_exception: bool = True,
        set_status_on_exception: bool = True,
    ) -> Span:
        """
        Same API as opentelemetry.trace.Tracer.start_span
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    def mark_rag_ingestion_trace_event(
        self,
        event: RAGIngestionEvent,
        # TODO: Add ability to add metadata in the event attributes
    ) -> RAGTraceEventResult:
        """
        Mark a RAGIngestionEvent in your ingestion trace. Each trace can contain
        multiple events, but can only contain each type of RAGIngestionEvent at
        most once. If you try to mark the same type of event multiple times in
        the same trace, this method returns a ValueError.

        These events get logged into the database connected to the
        LastMileTracerProvider when the trace is finished (exiting its root
        span).

        None of the events are strictly required to be included in your trace.
        If any of the events from RAGIngestionEvent were not marked they will
        be stored as an empty JSON.

        @param event (RAGIngestionEvent): An event object containing data about
            the state of the RAG LLM system

        @return RAGTraceEventResult: Flag indicating whether the event was
            marked successfully
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    def mark_rag_query_trace_event(
        self,
        event: RAGQueryEvent,
        # TODO: Add ability to add metadata in the event attributes
        indexing_trace_id: str | None = None,
        # TODO: Allow test_set_id to be a list so we can save this trace to
        # multiple test sets if we want
        # TODO: Add ability to link to test_set_id once test set API is built.
        # See https://github.com/lastmile-ai/eval/issues/113
        # test_set_id: str | None = None,
    ) -> RAGTraceEventResult:
        """
        Mark a RAGQueryEvent in your retrieval trace. Each trace can contain
        multiple events, but can only contain each type of RAGQueryEvent at
        most once. If you try to mark the same type of event multiple times in
        the same trace, this method returns a ValueError.

        These events get logged into the database connected to the
        LastMileTracerProvider when the trace is finished (exiting its root
        span).

        None of the events are strictly required to be included in your trace.
        If any of the events from RAGQueryEvent were not marked they will be
        stored as an empty JSON.

        @param event (RAGQueryEvent): An event object containing data about
            the state of the RAG LLM system
        @param test_set_id Optional(str): If traces are to be evaluated in the
            future, they can be grouped together under a test set where each
            trace (along with its marked RAG events) represents a single test
            case in that test set. The test set can be used to run evaluation
            metrics on each trace, as well as run aggregated metric
            evaluations afterwards. Defaults to None.
        @param indexing_trace_id Optional(str): The trace ID of a trace that
            was logged when previously running the ingestion (indexing and
            data storage) process for the documents used in the RAG retrieval
            step. Defaults to None.

        @return RAGTraceEventResult: Flag indicating whether the event was
            marked successfully
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def register_param(
        self,
        key: str,
        value: Any,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        Define the parameter K-V pair to save for the current trace instance

        @param key (str): The name of the parameter to be saved
        @param value (Any): The value of the parameter to be saved
        @param should_also_save_in_span (bool): Whether to also save this K-V
            pair in the current span attributes data. Defaults to true
        @param span Optional(Span): The span to save the K-V pair in
            addition to regular paramSet. This can be helpful for debugging
            when going through the trace. Only has an effect if
            should_also_save_in_span is true. Defaults to
            `trace_api.get_current_span()` which is the most recent span
            generated by calling tracer.start_as_current_span
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def get_params(self) -> dict[str, Any]:
        """
        Returns the params_dict that contains all the parameters that have been
        registered with a trace so far.
        """
        raise NotImplementedError("Not implemented directly, this is an API")
