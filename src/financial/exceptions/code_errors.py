from enum import Enum

class FinacialErrorTag(Enum):
    GENERIC = "generic"
    DATABASE_ADAPTER = "database_adapter"


class FinacialErrorGroup(Enum):
    GENERIC = "generic"
    USER = "user"
    TRANSACTION = "transaction"
    TRANSACTION_TAG = "transaction_tag"
    TRANSACTION_CATEGORY = "transaction_category"
    ACCOUNT = "account"
    ACCOUNT_TAG = "account_tag"


class FinacialErrorType(Enum):
    GENERIC = "GEN"
    NOT_FOUND = "404"
    CONNECTION = "CONN"
    INVALID_INPUT = "INV"
    PERMISSION = "PERM"
    ALREADY_EXISTS = "ALREADY_EXISTS"