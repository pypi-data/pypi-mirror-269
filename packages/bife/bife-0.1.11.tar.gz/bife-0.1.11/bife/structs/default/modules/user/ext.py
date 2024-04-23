# Control
class UserNotFound(Exception):
    ...


class UserAlreadyExists(Exception):
    ...


# Invalid
class InvalidUsername(Exception):
    ...


class InvalidEmail(Exception):
    ...


class InvalidGender(Exception):
    ...


class InvalidPassword(Exception):
    ...


class InvalidName(Exception):
    ...


# Login
class InvalidUserLogin(Exception):
    ...
