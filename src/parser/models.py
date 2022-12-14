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
    living_space: str | None = field(default=None)
    total_space: str | None = field(default=None)
    form_of_ownership: str | None = field(default=None)
    phone: str | None = field(default=None)
    email: str | None = field(default=None)
    registered_people: str | None = field(default=None)
    unavailable_people: str | None = field(default=None)
    indebtedness: str | None = field(default=None)
    indebtedness_info: str | None = field(default=None)
    fine: str | None = field(default=None)


@dataclass
class PaysHistory:
    data_income: str | None = field(default=None)
    amount: str | None = field(default=None)
    pay_agent: str | None = field(default=None)


@dataclass
class Counters:
    name: str | None = field(default=None)
    period: str | None = field(default=None)
    old: str | None = field(default=None)
