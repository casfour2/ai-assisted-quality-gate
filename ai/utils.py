import re


def extract_json(text: str) -> str:
    """
    Extract the first valid JSON object from a string.
    Raises ValueError if none found.
    """

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in AI response.")

    return match.group(0)