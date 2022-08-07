from dataclasses import dataclass, field


@dataclass
class Cookies:
    domain: str | None = field(default=None)
    http_only: bool | None = field(default=None)
    name: str | None = field(default=None)
    path: str | None = field(default=None)
    secure: bool | None = field(default=None)
    value: str | None = field(default=None)


@dataclass
class UserInformation:
    subscriber: str | None = field(default=None)
    address: str | None = field(default=None)
    living_space: float | None = field(default=None)
    total_space: float | None = field(default=None)
    form_of_ownership: str | None = field(default=None)
    phone: int | None = field(default=None)
    email: str | None = field(default=None)
    registered_people: int | None = field(default=None)
    unavailable_people: int | None = field(default=None)
    indebtedness: int | None = field(default=None)
    fines: int | None = field(default=None)
