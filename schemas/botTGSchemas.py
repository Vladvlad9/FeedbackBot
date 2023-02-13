from pydantic import BaseModel, Field


class BotTGSchema(BaseModel):
    user_id: int = Field(ge=1)
    bot_id: int = Field(ge=1)
    bot_token: str


class BotTGInDBSchema(BotTGSchema):
    id: int = Field(ge=1)
