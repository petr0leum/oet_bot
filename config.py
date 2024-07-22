from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar


class Settings(BaseSettings):
    model_config: ClassVar = SettingsConfigDict(
        case_sensitive=False
    )

    chat_model: str = "gpt-3.5-turbo-0125"  # "gpt-4o", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-0125"
    game_time: int = 5  # mins

    bot_token: str
    openai_api_token: str
    openai_proj_oet: str
    openai_org_id: str

settings = Settings()