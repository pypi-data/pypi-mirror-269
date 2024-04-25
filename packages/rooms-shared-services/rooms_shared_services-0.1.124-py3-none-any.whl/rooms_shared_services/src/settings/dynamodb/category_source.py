from rooms_shared_services.src.settings.dynamodb.base import BaseDynamodbSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseDynamodbSettings):
    model_config = SettingsConfigDict(env_prefix="product_category_source_")

    id_indexname: str
