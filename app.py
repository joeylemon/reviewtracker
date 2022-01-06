from flask import Flask, request, json, jsonify
from werkzeug.exceptions import HTTPException
from urllib.parse import urlparse
import utils
import errors

app = Flask(__name__)

@app.route("/reviews", methods=["POST", "GET"])
def get_reviews():
    """ Get all reviews under the given URL. """
    url = request.form.get("url")
    if url is None:
        url = "https://www.lendingtree.com/reviews/personal/first-midwest-bank/52903183?sort=&pid=2"
        # raise errors.MissingParameter("url parameter is missing")

    # extract domain name from URL (e.g. https://www.lendingtree.com/reviews => www.lendingtree.com)
    domain = urlparse(url).netloc

    # find the parser associated with this domain
    parser = utils.get_parser(domain)
    if not parser:
        raise errors.URLError(f"cannot get reviews: {domain} is not supported")

    reviews = parser.parse_url(url)
    response = jsonify(reviews)
    response.status_code = 200
    response.content_type = "application/json"
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    """ Display all errors during routing as JSON responses. """
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"

        return response
    else:
        response = jsonify({
            "code": 500,
            "name": e.__class__.__name__,
            "description": str(e)
        })
        response.status_code = 500
        response.content_type = "application/json"

        return response