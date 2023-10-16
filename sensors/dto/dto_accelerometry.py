from typing import Optional

from pydantic import Field
from sensors.dto.dto_entity import DtoEntity


class DtoAccelerometry(DtoEntity):
    x_acceleration: Optional[float] = Field(default=None)
    y_acceleration: Optional[float] = Field(default=None)
    z_acceleration: Optional[float] = Field(default=None)

    x_raw: Optional[float] = Field(default=None)
    y_raw: Optional[float] = Field(default=None)
    z_raw: Optional[float] = Field(default=None)

    x_offset: Optional[float] = Field(default=None)
    y_offset: Optional[float] = Field(default=None)
    z_offset: Optional[float] = Field(default=None)
    
    dropped: Optional[bool] = Field(default=None)
    tapped: Optional[bool] = Field(default=None)
    motion_detected: Optional[bool] = Field(default=None)
