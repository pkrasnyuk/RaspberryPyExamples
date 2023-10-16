import logging
from typing import Optional

import board
import digitalio

from sensors.dto.dto_motion import DtoMotion
from sensors.services.base_sensor_service import BaseSensorService


class MotionDetectionSensorService(BaseSensorService):
    def __init__(self, pin: Optional[int] = None):
        super().__init__(pin=pin)
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        if self._sensor_pin is not None and self._sensor_pin > 0:
            self.__sensor = digitalio.DigitalInOut(pin=self.__get_pin(value=self._sensor_pin))
            if self.__sensor is not None:
                self.__sensor.direction = digitalio.Direction.INPUT
            else:
                self.__logger.warning(msg="Failed to initialize Motion Detection sensor")
        else:
            self.__logger.error(msg="The pin value for Motion Detection sensor was not initialized")

    def get_sensor_data(self) -> Optional[DtoMotion]:
        if self.__sensor is not None:
            return DtoMotion(motion_detection=self.__sensor.value)
        else:
            self.__logger.warning(msg="Failed get data from Motion Detection sensor")
            return None

    def __get_pin(self, value: int):
        if value == 18:
            return board.D18
        elif value == 19:
            return board.D19
        else:
            return board.D0
