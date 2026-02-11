import re
import json


def extract_json(text: str) -> str:
    """
    Extract the first valid JSON object from a string.
    Normalizes whitespace/newlines within JSON values to prevent parsing errors.
    Raises ValueError if none found.
    """

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in AI response.")

    raw_json = match.group(0)

    try:
        parsed = json.loads(raw_json)
        return json.dumps(parsed)
    except json.JSONDecodeError:

        cleaned = re.sub(r'(?<=["\w])\n(?=[^"]*")', ' ', raw_json)
        try:
            parsed = json.loads(cleaned)
            return json.dumps(parsed)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON object: {e}") from e