from pydantic import (BaseModel, Extra)


class BaseInfuzuObject(BaseModel):
    class Config:
        extra = Extra.ignore
        arbitrary_types_allowed = True
