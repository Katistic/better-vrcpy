class RequestErrors:
    class NoSession(Exception):
        # Raised when trying to make a call without a session
        pass

    class SessionExists(Exception):
        # Raised when trying to make a second new session without closing the first
        pass

    class RequestError(Exception):
        # Raised when all request retry attempts fail
        pass

class ClientErrors:
    class OutOfDate(Exception):
        # Raised when apiKey is not in config
        pass

    class MissingCredentials(Exception):
        # Raised when Client.login is called without either username+password
        #   and base64
        pass
