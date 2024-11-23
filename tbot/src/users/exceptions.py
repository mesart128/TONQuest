class UserFlowException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__()

    pass


class UserAlreadyExistsException(UserFlowException):
    pass


class UserNotFoundException(UserFlowException):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with id {user_id} not found")
