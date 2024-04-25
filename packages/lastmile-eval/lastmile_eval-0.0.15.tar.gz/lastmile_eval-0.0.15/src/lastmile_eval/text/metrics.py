from textwrap import dedent
from typing import Any, Sequence

import pandas as pd

# Bleu
from evaluate import EvaluationModule, load  # type: ignore[fixme]

# phoenix arize
from phoenix.evals import (
    HUMAN_VS_AI_PROMPT_RAILS_MAP,
    HUMAN_VS_AI_PROMPT_TEMPLATE,
    QA_PROMPT_RAILS_MAP,
    QA_PROMPT_TEMPLATE,
    RAG_RELEVANCY_PROMPT_RAILS_MAP,
    RAG_RELEVANCY_PROMPT_TEMPLATE,
    TOXICITY_PROMPT_RAILS_MAP,
    TOXICITY_PROMPT_TEMPLATE,
    OpenAIModel,
    llm_classify,
)
from phoenix.evals.default_templates import (
    SUMMARIZATION_PROMPT_RAILS_MAP,
    SUMMARIZATION_PROMPT_TEMPLATE,
)

from lastmile_eval.text.metrics_lib import make_calculate_custom_llm_score


def calculate_bleu_score(
    texts_to_evaluate: Sequence[str], references: Sequence[str]
) -> list[float]:
    """
    Calculate BLEU scores for a set of hypotheses against corresponding sets of reference texts_to_evaluate.


    Args:
        texts_to_evaluate (Sequence[str]): The generated texts_to_evaluate to evaluate.
        references (Sequence[Sequence[str]]):
        The reference texts_to_evaluate for evaluation.
        Each set of references corresponds to one text.

    Returns:
        list[float]: A list of BLEU scores for each text-reference pair.

    Raises:
        ValueError: If the number of texts_to_evaluate and the number of sets of references are not equal.
    """

    if len(texts_to_evaluate) != len(references):
        raise ValueError(
            f"Number of predictions ({len(texts_to_evaluate)}) and references ({len(references)}) must be equal."
        )

    bleu_metric: EvaluationModule = load("bleu")

    def _score_pair(text: str, reference: str) -> float:
        results: dict[Any, Any] = bleu_metric.compute(  # type: ignore[fixme]
            predictions=[text], references=[[reference]]
        )
        return results["bleu"]

    return [
        _score_pair(text, reference)
        for text, reference in zip(texts_to_evaluate, references)
    ]


def calculate_exact_match_score(
    texts_to_evaluate: Sequence[str], references: Sequence[str]
) -> list[float]:
    """
    Calculate Exact Match score for a set of hypotheses against corresponding sets of reference texts_to_evaluate.


    Args:
        texts_to_evaluate (Sequence[str]): The generated texts_to_evaluate to evaluate.
        references (Sequence[Sequence[str]]):
        The reference texts_to_evaluate for evaluation.
        Each set of references corresponds to one text.

    Returns:
        list[float]: A list of Exact Match scores for each text-reference pair.

    Raises:
        ValueError: If the number of texts_to_evaluate and the number of sets of references are not equal.
    """

    if len(texts_to_evaluate) != len(references):
        raise ValueError(
            f"Number of predictions ({len(texts_to_evaluate)}) and references ({len(references)}) must be equal."
        )

    bleu_metric: EvaluationModule = load("exact_match")

    def _score_pair(text: str, reference: Sequence[str]) -> float:
        results: dict[Any, Any] = bleu_metric.compute(predictions=[text], references=[reference])  # type: ignore[no-untyped-call]
        return results["exact_match"]

    return [
        _score_pair(text, reference)
        for text, reference in zip(texts_to_evaluate, references)
    ]


def calculate_rouge1_score(
    texts_to_evaluate: Sequence[str], references: Sequence[Sequence[str]]
) -> list[float]:
    """
    Calculate Rouge-1 score for a set of hypotheses against corresponding sets of reference texts_to_evaluate.


    Args:
        texts_to_evaluate (Sequence[str]): The generated texts_to_evaluate to evaluate.
        references (Sequence[Sequence[str]]):
        The reference texts_to_evaluate for evaluation.
        Each set of references corresponds to one text.

    Returns:
        list[float]: A list of Rouge-1 scores for each text-reference pair.

    Raises:
        ValueError: If the number of texts_to_evaluate and the number of sets of references are not equal.
    """

    if len(texts_to_evaluate) != len(references):
        raise ValueError(
            f"Number of predictions ({len(texts_to_evaluate)}) and references ({len(references)}) must be equal."
        )

    bleu_metric: EvaluationModule = load("rouge")

    def _score_pair(text: str, reference: Sequence[str]) -> float:
        results: dict[Any, Any] = bleu_metric.compute(predictions=[text], references=[reference])  # type: ignore[no-untyped-call]
        return results["rouge1"]

    return [
        _score_pair(text, reference)
        for text, reference in zip(texts_to_evaluate, references)
    ]


def calculate_relevance_score(
    texts_to_evaluate: Sequence[str],
    references: Sequence[str],
    model_name: str = "gpt-3.5-turbo",
) -> list[float]:
    """
    Evaluates the relevance of input strings against reference strings using a specific evaluation model,
    and returns a list of float scores representing the relevance of each input-reference pair.

    Args:
        inputs (Sequence[str]): A sequence of input strings to be evaluated.
        references (Sequence[str]): A sequence of reference strings to evaluate the inputs against.

    Returns:
        List[float]: A list of float scores indicating the relevance of each input-reference pair,
                     where 1.0 denotes 'relevant' and 0.0 denotes otherwise.
    """
    openai_model = OpenAIModel(
        model=model_name,
        temperature=0.0,
    )

    return _calculate_relevance_score_helper(
        texts_to_evaluate, references, model_name, openai_model
    )


def _calculate_relevance_score_helper(
    texts_to_evaluate: Sequence[str],
    references: Sequence[str],
    model_name: str,
    openai_model: OpenAIModel,
):
    if len(texts_to_evaluate) != len(references):
        raise ValueError(
            f"Number of predictions ({len(texts_to_evaluate)}) and references ({len(references)}) must be equal."
        )

    if model_name not in ["gpt-3.5-turbo", "gpt-4"]:
        raise ValueError(
            f"Model name must be one of 'gpt-3.5-turbo' or 'gpt-4'."
        )
    # Create DataFrame
    df = pd.DataFrame({"input": texts_to_evaluate, "reference": references})

    guard_rails = list(RAG_RELEVANCY_PROMPT_RAILS_MAP.values())

    classification_results = llm_classify(
        df, openai_model, RAG_RELEVANCY_PROMPT_TEMPLATE, guard_rails
    )

    # Convert the classification results to a list of floats
    relevance_scores = [
        1.0 if label == "relevant" else 0.0
        for label in classification_results["label"].tolist()  # type: ignore[fixme]
    ]

    return relevance_scores


def calculate_toxicity_score(
    texts_to_evaluate: Sequence[str],
    model_name: str = "gpt-3.5-turbo",
) -> list[float]:
    """

    Args:
        texts_to_evaluate (Sequence[str]): A sequence of input strings to be evaluated.

    Returns:
        List[float]
    """
    openai_model = OpenAIModel(
        model=model_name,
        temperature=0.0,
    )

    return _calculate_toxicity_score_helper(
        texts_to_evaluate, model_name, openai_model
    )


def _calculate_toxicity_score_helper(
    texts_to_evaluate: Sequence[str],
    model_name: str,
    openai_model: OpenAIModel,
):
    if model_name not in ["gpt-3.5-turbo", "gpt-4"]:
        raise ValueError(
            f"Model name must be one of 'gpt-3.5-turbo' or 'gpt-4'."
        )
    # Create DataFrame
    df = pd.DataFrame({"input": texts_to_evaluate})

    guard_rails = list(TOXICITY_PROMPT_RAILS_MAP.values())

    classification_results = llm_classify(
        df, openai_model, TOXICITY_PROMPT_TEMPLATE, guard_rails
    )

    # Convert the classification results to a list of floats
    toxicity_scores = [
        1.0 if label == "toxic" else 0.0
        for label in classification_results["label"].tolist()  # type: ignore[fixme]
    ]

    return toxicity_scores


def calculate_qa_score(
    texts_to_evaluate: Sequence[str],
    references: Sequence[str],
    questions: Sequence[str],
    model_name: str = "gpt-3.5-turbo",
) -> list[float]:
    """

    Args:
        texts_to_evaluate (Sequence[str]): A sequence of input strings to be evaluated.

    Returns:
        List[float]
    """
    openai_model = OpenAIModel(
        model=model_name,
        temperature=0.0,
    )

    return _calculate_qa_score_helper(
        texts_to_evaluate, references, questions, model_name, openai_model
    )


def _calculate_qa_score_helper(
    texts_to_evaluate: Sequence[str],
    references: Sequence[str],
    questions: Sequence[str],
    model_name: str,
    openai_model: OpenAIModel,
):
    if len(texts_to_evaluate) != len(references) or len(
        texts_to_evaluate
    ) != len(questions):
        raise ValueError(
            f"Number of texts_to_evaluate ({len(texts_to_evaluate)}), references ({len(references)}), and questions ({len(questions)}) must be equal."
        )

    if model_name not in ["gpt-3.5-turbo", "gpt-4"]:
        raise ValueError(
            f"Model name must be one of 'gpt-3.5-turbo' or 'gpt-4'."
        )
    # Create DataFrame
    df = pd.DataFrame(
        {
            "input": questions,
            "reference": references,
            "output": texts_to_evaluate,
        }
    )

    guard_rails = list(QA_PROMPT_RAILS_MAP.values())

    classification_results = llm_classify(
        df, openai_model, QA_PROMPT_TEMPLATE, guard_rails
    )

    # Convert the classification results to a list of floats
    toxicity_scores = [
        1.0 if label == "correct" else 0.0
        for label in classification_results["label"].tolist()  # type: ignore[fixme]
    ]

    return toxicity_scores


def calculate_summarization_score(
    texts_to_evaluate: Sequence[str],
    references: Sequence[str],
    model_name: str = "gpt-3.5-turbo",
) -> list[float]:
    """
    Args:
        inputs (Sequence[str]): A sequence of input strings to be evaluated.
        references (Sequence[str]): A sequence of reference strings to evaluate the inputs against.

    Returns:
        List[float]: A list of float scores indicating the summary quality of each input-reference pair,
                     where 1.0 denotes 'good' and 0.0 denotes otherwise.
    """
    openai_model = OpenAIModel(
        model=model_name,
        temperature=0.0,
    )

    return _calculate_summarization_score_helper(
        texts_to_evaluate, references, model_name, openai_model
    )


def _calculate_summarization_score_helper(
    texts_to_evaluate: Sequence[str],
    references: Sequence[str],
    model_name: str,
    openai_model: OpenAIModel,
):
    if len(texts_to_evaluate) != len(references):
        raise ValueError(
            f"Number of texts_to_evaluate ({len(texts_to_evaluate)}) and references ({len(references)}) must be equal."
        )

    if model_name not in ["gpt-3.5-turbo", "gpt-4"]:
        raise ValueError(
            f"Model name must be one of 'gpt-3.5-turbo' or 'gpt-4'."
        )
    # Create DataFrame
    df = pd.DataFrame({"input": texts_to_evaluate, "output": references})

    guard_rails = list(SUMMARIZATION_PROMPT_RAILS_MAP.values())

    classification_results = llm_classify(
        df, openai_model, SUMMARIZATION_PROMPT_TEMPLATE, guard_rails
    )

    # Convert the classification results to a list of floats
    relevance_scores = [
        1.0 if label == "good" else 0.0
        for label in classification_results["label"].tolist()  # type: ignore[fixme]
    ]

    return relevance_scores


def calculate_human_vs_ai_score(
    texts_to_evaluate: Sequence[str],
    references: Sequence[str],
    questions: Sequence[str],
    model_name: str = "gpt-3.5-turbo",
) -> list[float]:
    """
    Args:
        inputs (Sequence[str]): A sequence of input strings to be evaluated.
        references (Sequence[str]): A sequence of reference strings to evaluate the inputs against.

    Returns:
        List[float]: A list of float scores indicating the summary quality of each input-reference pair,
                     where 1.0 denotes 'good' and 0.0 denotes otherwise.
    """
    openai_model = OpenAIModel(
        model=model_name,
        temperature=0.0,
    )

    return _calculate_human_vs_ai_score_helper(
        texts_to_evaluate, references, questions, model_name, openai_model
    )


def _calculate_human_vs_ai_score_helper(
    texts_to_evaluate: Sequence[str],
    references: Sequence[str],
    questions: Sequence[str],
    model_name: str,
    openai_model: OpenAIModel,
):
    if len(texts_to_evaluate) != len(references):
        raise ValueError(
            f"Number of predictions ({len(texts_to_evaluate)}) and references ({len(references)}) must be equal."
        )

    if model_name not in ["gpt-3.5-turbo", "gpt-4"]:
        raise ValueError(
            f"Model name must be one of 'gpt-3.5-turbo' or 'gpt-4'."
        )
    # Create DataFrame
    df = pd.DataFrame(
        {
            "ai_generated_answer": texts_to_evaluate,
            "correct_answer": references,
            "question": questions,
        }
    )

    guard_rails = list(HUMAN_VS_AI_PROMPT_RAILS_MAP.values())

    classification_results = llm_classify(
        df, openai_model, HUMAN_VS_AI_PROMPT_TEMPLATE, guard_rails
    )

    # Convert the classification results to a list of floats
    relevance_scores = [
        1.0 if label == "correct" else 0.0
        for label in classification_results["label"].tolist()  # type: ignore[fixme]
    ]

    return relevance_scores


def calculate_custom_llm_metric_example_sentiment(
    texts_to_evaluate: Sequence[str],
    model_name: str = "gpt-3.5-turbo",
) -> list[float]:
    """

    Args:
        texts_to_evaluate (Sequence[str]): The generated texts to evaluate.
        model_name (str): The name of the evaluation model to use.

    Returns:
        list[float]: A list of custom sentiment scores for each text.
    """

    prompt_template = dedent(
        """
        How happy is the following text on a scale of 0 to 1?
        {text_to_evaluate}
        """
    )

    input_names = ["text_to_evaluate"]
    scorer = make_calculate_custom_llm_score(
        prompt_template, model_name, input_names
    )
    return scorer(texts_to_evaluate)


def calculate_custom_llm_metric_example_semantic_similarity(
    texts_to_evaluate: Sequence[str],
    references: Sequence[str],
    model_name: str = "gpt-3.5-turbo",
) -> list[float]:
    """

    Args:
        texts_to_evaluate (Sequence[str]): The generated texts to evaluate.
        references (Sequence[str]): The reference texts to evaluate against.
        model_name (str): The name of the evaluation model to use.

    Returns:
        list[float]: A list of custom similarity scores for each text.
    """

    prompt_template = dedent(
        """
        How similar is the following text to the reference on a scale of 0 to 1
        
        Text: {text_to_evaluate}         
        Reference: {reference}
        """
    )

    input_names = ["text_to_evaluate", "reference"]
    scorer = make_calculate_custom_llm_score(
        prompt_template, model_name, input_names
    )
    return scorer(texts_to_evaluate, references)
