from enum import Enum


class TransactionTypes(Enum):
    EXPENSE = "despesa"
    INCOME = "renda"
    TRANSFER = "transferência"
    ADJUST = "ajuste"