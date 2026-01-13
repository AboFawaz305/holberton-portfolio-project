from profanityfilter import ProfanityFilter

pf = ProfanityFilter()


def is_spam(message: str) -> bool:
    return pf.is_profane(message)
