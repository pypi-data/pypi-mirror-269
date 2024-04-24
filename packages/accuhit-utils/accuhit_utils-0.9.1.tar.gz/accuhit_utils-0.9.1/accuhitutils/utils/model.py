from pydantic import BaseModel


class BaseSupportModel(BaseModel):
    class Config:
        populate_by_name = True
        use_enum_values = True
        from_attributes = True
        arbitrary_types_allowed = True
