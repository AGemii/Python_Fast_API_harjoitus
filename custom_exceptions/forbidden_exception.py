
class ForbiddenException(Exception):
    def __init__(self, message: str='forbidden') -> None:
        super().__init__(message)