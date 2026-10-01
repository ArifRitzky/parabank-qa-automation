import uuid
from dataclasses import dataclass


@dataclass
class UserData:
    first_name: str = "Budi"
    last_name: str = "QA"
    street: str = "Jl. Sudirman No 1"
    city: str = "Jakarta"
    state: str = "DKI"
    zip_code: str = "12345"
    phone: str = "08123456789"
    ssn: str = "32010123"
    username: str = ""
    password: str = "Password123!"

    @classmethod
    def unique(cls):
        """A user with a collision-free username (uuid-based, not random 4 digits)."""
        return cls(username=f"qa_{uuid.uuid4().hex[:10]}")
