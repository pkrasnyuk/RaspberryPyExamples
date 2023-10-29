from typing import Optional

from pydantic import Field

from sensors.dto.dto_entity import DtoEntity


class DtoGas(DtoEntity):
    co: Optional[float] = Field(default=None, serialization_alias="co")
    h2: Optional[float] = Field(default=None, serialization_alias="h2")
    ch4: Optional[float] = Field(default=None, serialization_alias="ch4")
    lpg: Optional[float] = Field(default=None, serialization_alias="lpg")
    propane: Optional[float] = Field(default=None, serialization_alias="propane")
    alcohol: Optional[float] = Field(default=None, serialization_alias="alcohol")
    smoke: Optional[float] = Field(default=None, serialization_alias="smoke")
