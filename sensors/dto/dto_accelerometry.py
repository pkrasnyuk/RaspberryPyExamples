from typing import Optional

from pydantic import Field

from sensors.dto.dto_entity import DtoEntity


class DtoAccelerometry(DtoEntity):
    x_acceleration: Optional[float] = Field(default=None, serialization_alias="x")
    y_acceleration: Optional[float] = Field(default=None, serialization_alias="y")
    z_acceleration: Optional[float] = Field(default=None, serialization_alias="z")

    x_raw: Optional[float] = Field(default=None, serialization_alias="x_raw")
    y_raw: Optional[float] = Field(default=None, serialization_alias="y_raw")
    z_raw: Optional[float] = Field(default=None, serialization_alias="z_raw")

    x_offset: Optional[float] = Field(default=None, serialization_alias="x_offset")
    y_offset: Optional[float] = Field(default=None, serialization_alias="y_offset")
    z_offset: Optional[float] = Field(default=None, serialization_alias="z_offset")

    dropped: Optional[bool] = Field(default=None, serialization_alias="dropped")
    tapped: Optional[bool] = Field(default=None, serialization_alias="tapped")
    motion_detected: Optional[bool] = Field(default=None, serialization_alias="motion")
