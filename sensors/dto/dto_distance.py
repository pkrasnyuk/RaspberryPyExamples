from typing import Optional

from pydantic import Field

from sensors.dto.dto_entity import DtoEntity


class DtoDistance(DtoEntity):
    distance: Optional[float] = Field(default=None, alias="distance")
