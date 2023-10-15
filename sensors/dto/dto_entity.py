from pydantic import BaseModel


class DtoEntity(BaseModel):
    pass

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        require_by_default = False
