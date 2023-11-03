from typing import Optional

from pydantic import Field

from sensors.dto.dto_entity import DtoEntity


class DtoSensor(DtoEntity):
    name: Optional[str] = Field(default=None)
    pin: Optional[int] = Field(default=None)

    def get_name(self) -> Optional[str]:
        return self.name

    def get_pin(self) -> Optional[int]:
        return self.pin
