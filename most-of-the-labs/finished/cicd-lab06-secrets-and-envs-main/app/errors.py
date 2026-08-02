"""HTTP error helpers, mirrors src/errors/HttpError.ts."""


class HttpError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.message = message

    @staticmethod
    def not_found(message: str = "Not found") -> "HttpError":
        return HttpError(404, message)

    @staticmethod
    def conflict(message: str = "Conflict") -> "HttpError":
        return HttpError(409, message)

    @staticmethod
    def bad_request(message: str = "Bad request") -> "HttpError":
        return HttpError(400, message)
