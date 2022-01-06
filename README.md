# reviewtracker
![Tests](https://github.com/joeylemon/reviewtracker/workflows/Tests/badge.svg)

A python web service to extract review details from LendingTree. Given a URL, this service will parse the page and return a JSON representation of the reviews. It uses [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/#) to parse the web page and regex to extract certain details. Additionally, it uses [Flask](https://flask.palletsprojects.com/) for creating a simple web service and [pytest](https://docs.pytest.org/) to define a test suite. 

For example, inputting the URL `https://www.lendingtree.com/reviews/personal/first-midwest-bank/52903183` will provide the following response:
```js
[
  {
    "author": "Brandon",
    "content": "Mrs. Navarrete was very professional and streamlined the process to make it easier on me. Highly recommend.Brandon",
    "date": "December 2021",
    "location": "Fayetteville,  NC",
    "stars": 5,
    "title": "Great experience"
  },
  {
    "author": "Douglas",
    "content": "The rates were excellent, the process was efficient and stress free. I was informed throughout the process and was impressed with the staff I was in contact with.",
    "date": "December 2021",
    "location": "Georgetown,  KY",
    "stars": 5,
    "title": "A very stress free and enjoyable experience"
  },
  // ... 8 more
]
```

## Usage
First, clone this repository and set up the virtual environment for the directory:
```sh
> git clone https://github.com/joeylemon/reviewtracker.git
> cd reviewtracker
> python3 -m venv venv
> source venv/bin/activate
```

Then, install the dependencies:
```sh
> pip install -r requirements.txt
```

You can now start the web service by running the `app.py` file:
```sh
> python app.py

Serving Flask app 'app' (lazy loading)
Environment: production
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
Debug mode: off
Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Testing
To test an individual URL, send a POST request to the `/reviews` endpoint of the web service with a parameter named `url`. For example:
```sh
> curl -X POST http://127.0.0.1:5000/reviews -d "url=https://www.lendingtree.com/reviews/personal/first-midwest-bank/52903183"
```

To run the test suite, use pytest on the `test/` directory like so:
```sh
python -m pytest test/ -v
```
