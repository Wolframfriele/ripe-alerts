class TokenNotValid(Exception):
    """Exception raised for error in the token.

    Attributes:
        token -- input token which caused the error
        message -- explanation of the error
    """

    def __init__(self, token):
        self.token = token
        self.message = "token not valid"
        super().__init__(self.message)

    def __str__(self):
        return f'{self.token} -> {self.message}'
