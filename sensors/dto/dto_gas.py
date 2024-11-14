from typing import Optional

from pydantic import Field

from sensors.dto.dto_entity import DtoEntity


class DtoGas(DtoEntity):
    co: Optional[float] = Field(default=None, alias="co")
    h2: Optional[float] = Field(default=None, alias="h2")
    ch4: Optional[float] = Field(default=None, alias="ch4")
    lpg: Optional[float] = Field(default=None, alias="lpg")
    propane: Optional[float] = Field(default=None, alias="propane")
    alcohol: Optional[float] = Field(default=None, alias="alcohol")
    smoke: Optional[float] = Field(default=None, alias="smoke")
