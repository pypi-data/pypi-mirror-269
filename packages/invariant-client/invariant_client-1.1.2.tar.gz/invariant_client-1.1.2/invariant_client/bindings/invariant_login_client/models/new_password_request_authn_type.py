from enum import Enum


class NewPasswordRequestAuthnType(str, Enum):
    PIN = "PIN"
    TOKEN = "TOKEN"

    def __str__(self) -> str:
        return str(self.value)
