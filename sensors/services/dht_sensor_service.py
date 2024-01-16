import logging
from typing import Optional

import adafruit_dht

from sensors.dto.dto_weather import DtoWeather
from sensors.services.base_sensor_service import BaseSensorService


class DHTSensorService(BaseSensorService):
    def __init__(self, pin: int):
        super().__init__(pin=pin)
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def get_sensor_data(self) -> Optional[DtoWeather]:
        if self._sensor_pin is not None and self._sensor_pin > 0:
            dht_sensor = adafruit_dht.DHT11(self._sensor_pin)
            if dht_sensor is not None:
                temperature = dht_sensor.temperature
                humidity = dht_sensor.humidity
                if humidity is not None and temperature is not None:
                    return DtoWeather(temperature=temperature, humidity=humidity)
                else:
                    self.__logger.warning(msg="Failed to retrieve data from DHT Sensor")
                    return None
            else:
                self.__logger.warning(msg="Failed for initialise DHT Sensor")
                return None
        else:
            self.__logger.error(msg="The pin value for DHT Sensor was not initialized")
            return None
