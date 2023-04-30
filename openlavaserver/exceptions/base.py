__all__ = ('ClientException',)


class ClientException(Exception):
    """The base exception for everything to do with clients."""

    message = "ClientException"

    def __init__(self, message=None):
        self.message = message or self.message
        super(ClientException, self).__init__(self.message)
