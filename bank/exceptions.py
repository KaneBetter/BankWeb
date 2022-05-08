class BankException(Exception):
    pass

class UserDoesNotExistOrWrongPassword(BankException):
    pass

class BalanceOverflow(BankException):
    pass

class UsernameExist(BankException):
    pass