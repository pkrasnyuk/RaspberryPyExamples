from typing import Optional

from pydantic import Field

from sensors.dto.dto_entity import DtoEntity


class DtoMotion(DtoEntity):
    motion_detection: Optional[bool] = Field(default=None, serialization_alias="motion")
