import logging
from typing import Optional

import board
import digitalio

from sensors.dto.dto_motion import DtoMotion
from sensors.services.base_sensor_service import BaseSensorService


class MotionDetectionSensorService(BaseSensorService):
    def __init__(self):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def get_sensor_data(self) -> Optional[DtoMotion]:
        if self._sensor_pin is not None and self._sensor_pin > 0:
            motion_sensor = digitalio.DigitalInOut(pin=self.__get_pin(value=self._sensor_pin))
            if motion_sensor is not None:
                motion_sensor.direction = digitalio.Direction.INPUT
                return DtoMotion(motion_detection=motion_sensor.value)
            else:
                self.__logger.warning(msg="Failed to initialize Motion Detection sensor")
                return None
        else:
            self.__logger.error(msg="The pin value for Motion Detection sensor was not initialized")
            return None

    def __get_pin(self, value: int):
        if value == 18:
            return board.D18
        elif value == 19:
            return board.D19
        else:
            return board.D0
