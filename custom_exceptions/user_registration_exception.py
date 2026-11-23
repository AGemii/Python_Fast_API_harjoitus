
class UserRegistrationException(Exception):
    def __init__(self, message: str='error registering user') -> None:
        super().__init__(message)