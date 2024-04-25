from enum import Enum
from uuid import UUID, uuid4

from pydantic import Field

from rooms_shared_services.src.models.texts.languages import Language
from rooms_shared_services.src.storage.models import BaseDynamodbModel


class AttributeVariant(Enum):
    FURNITURE_TYPES = "FURNITURE_TYPES"
    MATERIALS = "MATERIALS"
    COUNTRY_OF_ORIGIN = "COUNTRY_OF_ORIGIN"
    DELIVERY_TERM = "DELIVERY_TERM"


class ProductAttribute(BaseDynamodbModel):
    id: UUID = Field(default_factory=uuid4)
    attr_language: Language
    attr_name: str
    attr_terms: list[str]
