from typing import Optional

from pydantic import Field
from sensors.dto.dto_entity import DtoEntity


class DtoWeather(DtoEntity):
    temperature: Optional[float] = Field(default=None)
    humidity: Optional[float] = Field(default=None)
    