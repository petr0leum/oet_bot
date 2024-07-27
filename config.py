from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar


class Settings(BaseSettings):
    model_config: ClassVar = SettingsConfigDict(
        case_sensitive=False
    )

    chat_model: str = "gpt-3.5-turbo-0125"
    game_time: int = 5 # speaking time
    time_to_read_card: int = 3 # preparaion time
    card_examples_num: int = 3 # amount of card examples to use in prompt

    bot_token: str
    openai_api_token: str = "default_api_token"
    openai_proj_oet: str = "default_project"
    openai_org_id: str = "default_org_id"
    
settings = Settings()