from dataclasses import dataclass


@dataclass
class Cookies:
    domain: str | None
    http_only: bool | None
    name: str | None
    path: str | None
    secure: bool | None
    value: str | None
