from parsers.review_parser import ReviewParser
from parsers.lendingtree import LendingTreeParser

# Map domain names to their respective parser function
# Omit "www." prefix from domain names
parsers = { "lendingtree.com": LendingTreeParser }

def get_parser(domain: str) -> ReviewParser:
    """ Get the parser for the given domain. """
    domain = domain.replace("www.", "")
    if domain in parsers:
        return parsers[domain]
    else:
        return None