import re
import requests
from bs4 import BeautifulSoup, element
from parsers.review_parser import ReviewParser
import errors


class LendingTreeParser(ReviewParser):
    def parse_url(url: str) -> list:
        """ Parse the given LendingTree URL to extract all reviews. """
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise errors.URLError(f"could not parse url: {e}", code=404)

        soup = BeautifulSoup(req.content, 'html.parser')
        reviewDivs = soup.select(".mainReviews")

        # if there isn't a div called .mainReviews, it's probably the wrong page
        if len(reviewDivs) == 0:
            raise errors.ReviewsError(f"no reviews found under url {url}")

        reviews = []
        for i, div in enumerate(reviewDivs):
            try:
                review = LendingTreeReviewElement(div)
                reviews.append(review.to_dict())
            except errors.ReviewsError as e:
                # ignore a single failure and continue parsing the rest
                print(f"failed to parse review {i}: {e}")

        # if every review failed to parse, something is wrong with the parsing
        if len(reviews) == 0:
            raise errors.ReviewsError(f"failed to parse any reviews under url {url}")

        return reviews


class LendingTreeReviewElement():
    """ An object representing a LendingTree review post given the parent div. """
    def __init__(self, div: element.Tag):
        self.div = div

    def to_dict(self) -> dict:
        return {
            "title": self.title(),
            "content": self.content(),
            "author": self.author(),
            "location": self.location(),
            "stars": self.stars(),
            "date": self.date()
        }

    def title(self) -> str:
        titleDiv = self.div.select_one(".reviewTitle")
        if not titleDiv:
            raise errors.ReviewsError(f"could not find title")

        return titleDiv.text.strip()

    def content(self) -> str:
        textDiv = self.div.select_one(".reviewText")
        if not textDiv:
            raise errors.ReviewsError(f"could not find content")

        return textDiv.text.strip()

    def author(self) -> str:
        authorDiv = self.div.select_one(".consumerName")
        if not authorDiv:
            raise errors.ReviewsError(f"could not find author")

        try:
            regex = re.search('(.*) from (.*)', authorDiv.text)
            author = regex.group(1)
        except ValueError:
            raise errors.ReviewsError(f"author element {authorDiv.text} is malformed")

        return author.strip()

    def location(self) -> str:
        authorDiv = self.div.select_one(".consumerName")
        if not authorDiv:
            raise errors.ReviewsError(f"could not find location")

        try:
            regex = re.search('(.*) from (.*)', authorDiv.text)
            location = regex.group(2)
        except ValueError:
            raise errors.ReviewsError(f"location element {authorDiv.text} is malformed")

        return location.strip()

    def stars(self) -> int:
        starsDiv = self.div.select_one(".numRec")
        if not starsDiv:
            raise errors.ReviewsError(f"could not find stars")

        try:
            regex = re.search('\((\d{1}) of 5\)stars', starsDiv.text)
            stars = int(regex.group(1))
        except ValueError:
            raise errors.ReviewsError(f"stars element {starsDiv.text} is malformed")

        return stars

    def date(self) -> str:
        dateDiv = self.div.select_one(".consumerReviewDate")
        if not dateDiv:
            raise errors.ReviewsError(f"could not find date")

        # use regex to extract date
        try:
            regex = re.search('Reviewed in (.*)', dateDiv.text)
            date = regex.group(1)
        except ValueError:
            raise errors.ReviewsError(f"date element {dateDiv.text} is malformed")

        return date.strip()