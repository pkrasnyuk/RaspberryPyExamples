from typing import Optional

from pydantic import Field

from sensors.dto.dto_entity import DtoEntity


class DtoGas(DtoEntity):
    co: Optional[float] = Field(default=None)
    h2: Optional[float] = Field(default=None)
    ch4: Optional[float] = Field(default=None)
    lpg: Optional[float] = Field(default=None)
    propane: Optional[float] = Field(default=None)
    alcohol: Optional[float] = Field(default=None)
    smoke: Optional[float] = Field(default=None)
