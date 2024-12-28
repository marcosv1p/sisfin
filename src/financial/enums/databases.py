from enum import Enum


class Databases(Enum):
    USERS = "user"
    ACCOUNTS = "account"
    ACCOUNTS_TAGS = "account_tag"
    TRANSACTIONS = "transaction"
    TRANSACTIONS_TAGS = "transaction_tag"
    TRANSACTIONS_CATEGORIES = "transaction_category"