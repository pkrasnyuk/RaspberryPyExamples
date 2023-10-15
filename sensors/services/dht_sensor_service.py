import logging
from typing import Optional

import Adafruit_DHT

from sensors.dto.dto_weather import DtoWeather
from sensors.services.base_sensor_service import BaseSensorService


class DHTSensorService(BaseSensorService):
    def __init__(self):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__dht_sensor = Adafruit_DHT.DHT11
        self.__delay_seconds = 10

    def get_sensor_data(self) -> Optional[DtoWeather]:
        if self._sensor_pin is not None and self._sensor_pin > 0:
            humidity, temperature = Adafruit_DHT.read_retry(
                sensor=self.__dht_sensor, pin=self._sensor_pin, delay_seconds=self.__delay_seconds
            )

            if humidity is not None and temperature is not None:
                return DtoWeather(temperature=temperature, humidity=humidity)
            else:
                self.__logger.warning(msg="Failed to retrieve data from DHT sensor")
                return None
        else:
            self.__logger.error(msg="The pin value for DHT sensor was not initialized")
            return None
