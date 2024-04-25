from pydantic import Field
from ..base import BaseInfuzuObject


class MarketingPreference(BaseInfuzuObject):
    cogitobot_marketing_updates: bool | None = Field(frozen=True)

    @classmethod
    def field_names(cls) -> list[str]:
        return list(cls.model_fields.keys())
