import logging
from typing import Optional

import adafruit_dht
import board

from sensors.dto.dto_weather import DtoWeather
from sensors.services.base_sensor_service import BaseSensorService


class DHTSensorService(BaseSensorService):
    def __init__(self, pin: int):
        super().__init__(pin=pin)
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        self.__dht_sensor = None
        if self._sensor_pin is not None and self._sensor_pin > 0:
            if self._sensor_pin == 18:
                self.__dht_sensor = adafruit_dht.DHT11(board.D18)
            elif self._sensor_pin == 19:
                self.__dht_sensor = adafruit_dht.DHT11(board.D19)
            else:
                self.__dht_sensor = adafruit_dht.DHT11(board.D27)
        else:
            self.__logger.error(msg="The pin value for DHT Sensor was not initialized")

    def get_sensor_data(self) -> Optional[DtoWeather]:
        if self.__dht_sensor is not None:
            try:
                temperature = self.__dht_sensor.temperature
                humidity = self.__dht_sensor.humidity
                if humidity is not None and temperature is not None:
                    return DtoWeather(temperature=temperature, humidity=humidity)
                else:
                    self.__logger.warning(msg="Failed to retrieve data from DHT Sensor")
            except RuntimeError as e:
                self.__logger.error(msg=f"Reading from DHT Sensor failure: {e.args}")
        else:
            self.__logger.warning(msg="Failed for initialise DHT Sensor")

        return None
