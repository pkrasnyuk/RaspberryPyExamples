from typing import List, Optional

from pydantic import Field

from sensors.dto.dto_entity import DtoEntity
from sensors.dto.dto_sensor import DtoSensor


class DtoSchedulerJob(DtoEntity):
    name: Optional[str] = Field(default=None)
    sensors: Optional[List[DtoSensor]] = Field(default=None)
    cron: Optional[str] = Field(default=None)

    def get_name(self) -> Optional[str]:
        return self.name

    def get_sensors(self) -> Optional[List[DtoSensor]]:
        return self.sensors

    def get_crontab(self) -> Optional[str]:
        return self.cron
