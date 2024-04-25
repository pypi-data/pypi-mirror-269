class WatrApiInvalidTokenException(Exception):
    """
    Exception raised when the token is invalid.
    """

    def __init__(self, message, errors=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.errors = errors
