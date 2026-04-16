def format_response(raw_response: str) -> dict:
    """
    Formats the AI response into structured parts:
    - Explanation
    - Example
    """

    explanation = ""
    example = ""

    try:
        # Split based on expected structure
        parts = raw_response.split("Example:")

        if len(parts) == 2:
            explanation = parts[0].replace("Explanation:", "").replace("*", "").strip()
            example = parts[1].replace("**", "").strip()
        else:
            # fallback if structure breaks
            explanation = raw_response.strip()
            example = "No example provided."

    except Exception:
        explanation = raw_response.strip()
        example = "Formatting error."

    return {
        "explanation": explanation,
        "example": example
    }