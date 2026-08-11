from typing import List


def classify_categories(content: str) -> List[str]:
    # Placeholder for Category Classification logic.
    # Could be ML-based or rule-based.
    categories = []
    content_lower = content.lower()
    if 'politics' in content_lower:
        categories.append('Politics')
    if 'economy' in content_lower or 'finance' in content_lower:
        categories.append('Economy')
    if 'sports' in content_lower:
        categories.append('Sports')
    if 'technology' in content_lower or 'tech' in content_lower:
        categories.append('Technology')
    if len(categories) == 0:
        categories.append('General')
    return categories
