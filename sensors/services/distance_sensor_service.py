import logging
from typing import Optional

from gpiozero import DistanceSensor

from sensors.dto.dto_distance import DtoDistance
from sensors.services.base_sensor_service import BaseSensorService


class DistanceSensorService(BaseSensorService):
    def __init__(self, pin: int, sub_pin: int):
        super().__init__(pin=pin, sub_pin=sub_pin)
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        if self._sensor_pin is not None and self._sensor_pin > 0:
            self.__sensor = DistanceSensor(
                trigger=self._sensor_pin, echo=self._sensor_sub_pin, max_distance=1, threshold_distance=0.2
            )
        else:
            self.__logger.error(msg="The pin value for Distance Sensor was not initialized")

    def get_sensor_data(self) -> Optional[DtoDistance]:
        if self.__sensor is not None:
            distance = self.__sensor.distance
            if distance is not None:
                return DtoDistance(distance=distance)
            else:
                self.__logger.warning(msg="Failed to get data from Distance Sensor")
                return None
        else:
            self.__logger.warning(msg="Failed get data from Distance Sensor")
            return None
