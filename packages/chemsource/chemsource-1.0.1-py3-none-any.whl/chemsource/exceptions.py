class XMLParseError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)

class XMLParseError2(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)

class XMLRetrievalError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)

class XMLRetrievalError2(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)

class JoinError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)

class DescriptionError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(message)