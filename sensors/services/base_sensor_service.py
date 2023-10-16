from abc import abstractmethod
from typing import Optional

from sensors.dto.dto_entity import DtoEntity
from sensors.services.base_service import BaseService


class BaseSensorService(BaseService):
    def __init__(self, pin: Optional[int] = None):
        self._sensor_pin = pin

    @abstractmethod
    def get_sensor_data(self) -> Optional[DtoEntity]:
        pass
