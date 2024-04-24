from dataclasses import dataclass


@dataclass
class AuthResponse:
    expires_at: int
    access_token: str


@dataclass
class TopicResponse:
    Id: int
    Type: int | None
    Title: str | None
    ShortTitle: str | None
    LastModifiedDate: str | None


@dataclass
class ModuleResponse:
    Id: int
    Type: int
    Title: str | None
    IsHidden: bool | None
    IsLocked: bool | None
    Structure: list[TopicResponse]
    ShortTitle: str | None
    ModuleEndDate: str | None
    ModuleDueDate: str | None
    ModuleStartDate: str | None
    LastModifiedDate: str | None
