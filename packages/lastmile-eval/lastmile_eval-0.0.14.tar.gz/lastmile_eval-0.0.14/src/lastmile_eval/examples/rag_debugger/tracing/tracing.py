"""
Example file showing how to use the SDK to create a tracer object and 
register parameters
"""

import json
import os
from typing import Any

from openinference.semconv.trace import (
    OpenInferenceSpanKindValues,
    SpanAttributes,
)
from opentelemetry import trace as trace_api
from opentelemetry.trace import StatusCode

from lastmile_eval.rag.debugger.api import LastMileTracer, QueryReceived

# TODO: Add these both to the API library instead of relying on SDK
from lastmile_eval.rag.debugger.tracing import (
    list_ingestion_trace_events,
    get_lastmile_tracer,
    get_latest_ingestion_trace_id,
    get_trace_data,
)

# Define a LastMileTracer, which contains the same base functions as a regular
# OpenTelemetry object
OUTPUT_FILE_NAME = "span_data.txt"
OUTPUT_FILE_PATH = os.path.join(os.path.dirname(__file__), OUTPUT_FILE_NAME)

# Define a LastMileTracer, which contains the same API interface as an
# OpenTelemetry tracer
tracer: LastMileTracer = get_lastmile_tracer(
    tracer_name="my-tracer",
    initial_params={"motivation_quote": "I love staring into the sun"},
    # output_filepath=OUTPUT_FILE_PATH,
)

# We do not have an existing trace running so this parameter will be registered
# to all subsequent traces
tracer.register_param("prognosis", "My eyes are burning!")


# Same tracer functionality for logging spans as usual for OpenTelemetry
@tracer.start_as_current_span(
    "ingestion-root-span"  # Span finishes automatically when retrieval_function ends
)
def ingestion_function():  # pylint: disable=missing-function-docstring
    root_span = trace_api.get_current_span()
    root_span.set_attribute(
        SpanAttributes.OPENINFERENCE_SPAN_KIND,
        OpenInferenceSpanKindValues.EMBEDDING.value,
    )
    print("We are in the ingestion root span now ")

    # Can also use embedded with-blocks instead of decorators around methods
    with tracer.start_as_current_span(
        "ingestion-child-span"
    ) as ingestion_child_span:
        print("We are in the ingestion child span now ")
        ingestion_child_span.set_attribute(
            SpanAttributes.OPENINFERENCE_SPAN_KIND,
            OpenInferenceSpanKindValues.CHAIN.value,
        )

        # Example of logging a RAG ingestion event
        log_result = tracer.mark_rag_ingestion_trace_event(
            event="Ingestion started"
        )
        print(log_result)

        # This parameter has the same key as something that's already stored
        # at the tracer level (one level above current trace). We will
        # overwrite the K-V pair for the trace-specific params, but when we
        # create a new trace the old value will remain
        tracer.register_param("chunk_size", 9000)

        ingestion_child_span.set_status(StatusCode.OK)


@tracer.start_as_current_span(
    "root-span"  # Span finishes automatically when retrieval_function ends
)
def retrieval_function():  # pylint: disable=missing-function-docstring
    root_span = trace_api.get_current_span()
    root_span.set_attribute(
        SpanAttributes.OPENINFERENCE_SPAN_KIND,
        OpenInferenceSpanKindValues.AGENT.value,
    )

    # Can also use embedded with-blocks instead of decorators around methods
    with tracer.start_as_current_span("child-span") as child_span:
        child_span.set_attribute(
            SpanAttributes.OPENINFERENCE_SPAN_KIND,
            OpenInferenceSpanKindValues.CHAIN.value,
        )
        words_of_wisdom: str = (
            "Maybe you shouldn't stare directly into the sun after all"
        )

        # Example of logging a RAG query event
        log_result = tracer.mark_rag_query_trace_event(
            event=QueryReceived(query="Is it healthy to stare at the sun?"),
            # test_set_id=str(1234),
            indexing_trace_id=str(5678),
        )
        print(log_result)

        # Example of registering another param
        tracer.register_param("words_of_wisdom", words_of_wisdom)

        # This parameter has the same key as something that's already stored
        # at the tracer level (one level above current trace). We will
        # overwrite the K-V pair for the trace-specific params, but when we
        # create a new trace the old value will remain
        tracer.register_param(
            "prognosis", "My eyes are super cool and fresh, no problems here!"
        )

        child_span.set_status(StatusCode.OK)


if __name__ == "__main__":
    # ingestion_function()
    # retrieval_function()
    # with tracer.start_as_current_span("new-root-span") as unconnected_span:
    #     manual_span_example = tracer.start_span("new-child-span")
    #     tracer.register_param(
    #         "new_param",
    #         "new_value",
    #         should_also_save_in_span=True,
    #         span=manual_span_example,
    #     )
    #     manual_span_example.end()
    #     unconnected_span.set_status(StatusCode.OK)

    #     print("This is the tracer.get_params() output:")
    #     print(json.dumps(tracer.get_params(), indent=4))

    # Example of getting trace data
    most_recent_ingestion_trace_id: str = get_latest_ingestion_trace_id()
    print(f"{most_recent_ingestion_trace_id=}")
    ingestion_trace_event_data: dict[str, Any] = get_trace_data(
        # TODO (optional): Add back context object for keep track of trace_ids
        # instead of hardcoding in this example
        trace_id=most_recent_ingestion_trace_id,  # Hard-coded for now
    )
    print(json.dumps(ingestion_trace_event_data, indent=4))
