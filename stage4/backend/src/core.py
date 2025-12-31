
"""Core search logic and mock data for the API."""

from typing import Dict, List

# Mock data set to simulate stored courses/groups.
# In a real application this would be replaced by a database query.
GROUPS: List[Dict[str, str | list[str]]] = [
    {
        "id": "grp-web-101",
        "name": "Web Development Bootcamp",
        "description": "HTML, CSS, and JavaScript fundamentals for beginners.",
        "keywords": ["web", "frontend", "javascript", "html", "css"],
    },
    {
        "id": "grp-python-data",
        "name": "Python for Data Analysis",
        "description": "Pandas, NumPy, and visualization workflows.",
        "keywords": ["python", "data", "pandas", "analytics"],
    },
    {
        "id": "grp-mobile-ux",
        "name": "Mobile UX Research",
        "description": "Qualitative and quantitative user research for "
        "mobile apps.",
        "keywords": ["mobile", "ux", "research", "design"],
    },
    {
        "id": "grp-backend-fastapi",
        "name": "FastAPI Backend Patterns",
        "description": "Building APIs with FastAPI and best practices.",
        "keywords": ["backend", "fastapi", "api", "python"],
    },
    {
        "id": "grp-devops-intro",
        "name": "Intro to DevOps",
        "description": "CI/CD pipelines, containers, and monitoring basics.",
        "keywords": ["devops", "ci", "cd", "containers", "docker"],
    },
]


def search_groups(keyword: str) -> List[Dict[str, str | list[str]]]:
    """
    Return groups whose name, description, or keywords include the
    provided term.

    The search is case-insensitive and performs simple substring matching.
    """
    term = keyword.strip().lower()
    if not term:
        return []

    results: List[Dict[str, str | list[str]]] = []
    for group in GROUPS:
        name_hit = term in group["name"].lower()
        desc_hit = term in group["description"].lower()
        keyword_hit = any(term in kw.lower() for kw in group["keywords"])
        if name_hit or desc_hit or keyword_hit:
            results.append(group)
    return results
