from functools import partial
from typing import Any, Protocol, Sequence

import pandas as pd
from pydantic import BaseModel

from .openai_batch_lib import (
    OpenAIClientConfig,
    RealOpenAIClientConfig,
    batch_run_df_to_structured,
    make_openai_default_text_to_structured,
)


class CustomTextMetric(Protocol):
    def __call__(self, *texts: Sequence[str]) -> list[float]:
        ...


def _custom_score_record_to_record(
    record: dict[Any, Any],  # TODO: fix this
    model_name: str,
    prompt_template: str,
    client_config: OpenAIClientConfig,
    **kwargs: Any,  # TODO: fix this
) -> dict[Any, Any]:
    prompt = prompt_template.format(**record)

    class Score(BaseModel):
        score: float

    text_to_structured = make_openai_default_text_to_structured(client_config)
    out = text_to_structured(prompt, model_name, Score, **kwargs)
    return out


def make_calculate_custom_llm_score(
    prompt_template: str, model_name: str, input_names: list[str]
) -> CustomTextMetric:
    client_config = RealOpenAIClientConfig()
    return _make_calculate_custom_llm_score_helper(
        prompt_template, model_name, input_names, client_config
    )


def _make_calculate_custom_llm_score_helper(
    prompt_template: str,
    model_name: str,
    input_names: list[str],
    client_config: OpenAIClientConfig,
) -> CustomTextMetric:
    def _metric(*texts: Sequence[str]) -> list[float]:
        if len(texts) != len(input_names):
            raise ValueError(
                f"Number of texts ({len(texts)}) does not match number of input names ({len(input_names)})"
            )
        df_in = pd.DataFrame(dict(zip(input_names, texts)))
        df_out = batch_run_df_to_structured(
            df_in,
            partial(
                _custom_score_record_to_record,
                prompt_template=prompt_template,
                model_name=model_name,
                client_config=client_config,
            ),
        )
        out = df_out["score"].astype(float)  # type: ignore[pandas]
        return out.tolist()  # type: ignore[pandas]

    return _metric
