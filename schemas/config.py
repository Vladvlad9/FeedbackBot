from pydantic import BaseModel


class BotSchema(BaseModel):
    TOKEN: list[str]
    ADMINS: list[int]


class CounterSchema(BaseModel):
    USER_MESSAGE: int
    ADMIN_MESSAGE: int


class ConfigSchema(BaseModel):
    BOT: BotSchema
    DATABASE: str
    COUNTER: CounterSchema
    CHAT: list[str]
