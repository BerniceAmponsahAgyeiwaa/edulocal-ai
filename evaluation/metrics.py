import json
from prompts.prompt_builder import build_prompt
from services.llm_service import get_ai_response


def keyword_match_score(response: str, keywords: list) -> float:
    """
    Simple evaluation metric:
    Checks how many expected keywords appear in response.
    """

    response_lower = response.lower()
    matches = sum(1 for kw in keywords if kw in response_lower)

    return matches / len(keywords)


def evaluate_model(dataset_path="evaluation/golden_dataset.json"):
    """
    Runs evaluation on golden dataset.
    """

    with open(dataset_path, "r") as f:
        dataset = json.load(f)

    scores = []

    for item in dataset:
        question = item["question"]
        keywords = item["expected_keywords"]

        messages = build_prompt(question)
        response = get_ai_response(messages)

        score = keyword_match_score(response, keywords)
        scores.append(score)

        print(f"\nQuestion: {question}")
        print(f"Score: {score:.2f}")

    avg_score = sum(scores) / len(scores)
    print(f"\nAverage Score: {avg_score:.2f}")