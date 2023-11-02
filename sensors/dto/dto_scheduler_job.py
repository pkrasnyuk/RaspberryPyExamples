from typing import Optional
from pydantic import Field
from sensors.dto.dto_entity import DtoEntity


class DtoSchedulerJob(DtoEntity):
    name: str = Field(default="")
    pin: Optional[int] = Field(default=None)
    sub_pin: Optional[int] = Field(default=None)
    cron: Optional[str] = Field(default=None)

    def get_crontab(self) -> Optional[str]:
        return self.cron
    
    def get_pin(self) -> Optional[int]:
        return self.pin
    
    def get_sub_pin(self) -> Optional[int]:
        return self.sub_pin
