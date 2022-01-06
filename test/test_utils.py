import pytest
import utils
from parsers.lendingtree import LendingTreeParser

def test_get_parser():
    """ Ensure the get_parser function returns a valid parser object or None if invalid domain. """
    parser = utils.get_parser("lendingtree.com")
    assert parser is LendingTreeParser

    parser = utils.get_parser("google.com")
    assert parser is None