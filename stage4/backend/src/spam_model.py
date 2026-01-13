"""Provide methods to deal with spam messages
"""
from profanityfilter import ProfanityFilter

pf = ProfanityFilter()


def is_spam(message: str) -> bool:
    """Return true if the message is considered a spam
    """
    return pf.is_profane(message)
