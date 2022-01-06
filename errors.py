from werkzeug.exceptions import HTTPException

class MissingParameter(HTTPException):
    name = "MissingParameter"
    code = 400

    def __init__(self, description, name=None, code=None):
        HTTPException.__init__(self)
        self.description = description
        if name is not None:
            self.name = name
        if code is not None:
            self.code = code

class URLError(HTTPException):
    name = "URLError"
    code = 400

    def __init__(self, description, name=None, code=None):
        HTTPException.__init__(self)
        self.description = description
        if name is not None:
            self.name = name
        if code is not None:
            self.code = code

class ReviewsError(HTTPException):
    name = "ReviewsError"
    code = 404

    def __init__(self, description, name=None, code=None):
        HTTPException.__init__(self)
        self.description = description
        if name is not None:
            self.name = name
        if code is not None:
            self.code = code