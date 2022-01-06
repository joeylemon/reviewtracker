import pytest
import json
from flask import testing
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_parse_reviews(client: testing.FlaskClient):
    """ Ensure the reviews are being parsed from the LendingTree URL. """
    resp = client.post("/reviews", data={"url": "https://www.lendingtree.com/reviews/personal/first-midwest-bank/52903183?sort=&pid=1"})
    reviews = json.loads(resp.data)
    assert len(reviews) > 0
    for review in reviews:
        assert "title" in review
        assert len(review["title"]) > 0
        
        assert "content" in review
        assert len(review["content"]) > 0

        assert "author" in review
        assert len(review["author"]) > 0

        assert "location" in review
        assert len(review["location"]) > 0

        assert "stars" in review
        assert 5 >= review["stars"] >= 0

        assert "date" in review
        assert len(review["date"]) > 0


def test_page_reviews(client: testing.FlaskClient):
    """ Ensure different reviews are parsed for different pages. """
    resp = client.post("/reviews", data={"url": "https://www.lendingtree.com/reviews/personal/first-midwest-bank/52903183?sort=&pid=1"})
    page1 = json.loads(resp.data)
    assert len(page1) > 0

    resp = client.post("/reviews", data={"url": "https://www.lendingtree.com/reviews/personal/first-midwest-bank/52903183?sort=&pid=2"})
    page2 = json.loads(resp.data)
    assert len(page2) > 0

    for i in range(max(len(page1), len(page2))):
        assert page1[i]["content"] != page2[i]["content"]
