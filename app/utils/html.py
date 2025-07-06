import re


def strip_tags(text: str) -> str:
    """Strips all HTML in a string.

    Args:
        text (str): HTML string with its tags.

    Returns:
        str: String without HTML tags.
    """
    return re.sub('<[^<]+?>', '', text)
