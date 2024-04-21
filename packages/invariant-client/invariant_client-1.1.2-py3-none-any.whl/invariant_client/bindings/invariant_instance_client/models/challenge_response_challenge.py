from enum import Enum


class ChallengeResponseChallenge(str, Enum):
    BASIC_AUTH = "basic_auth"
    NEW_PASSWORD = "new_password"
    RESET_PIN = "reset_pin"
    VALIDATE_EMAIL = "validate_email"

    def __str__(self) -> str:
        return str(self.value)
