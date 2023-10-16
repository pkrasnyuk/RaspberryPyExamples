import logging
from typing import Optional

from gas_detection import GasDetection

from sensors.dto.dto_gas import DtoGas
from sensors.services.base_sensor_service import BaseSensorService


class GazSensorService(BaseSensorService):
    def __init__(self, pin: Optional[int] = None):
        super().__init__(pin=pin)
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        if self._sensor_pin is not None and self._sensor_pin > 0:
            self.__sensor = GasDetection(pin=self._sensor_pin)
            if self.__sensor is not None:
                self.__sensor.calibrate()
            else:
                self.__logger.warning(msg="Failed to initialize Gas Detection sensor")
        else:
            self.__logger.error(msg="The pin value for Gas Detection sensor was not initialized")

    def get_sensor_data(self) -> Optional[DtoGas]:
        if self.__sensor is not None:
            ppm: dict = self.__sensor.percentage()
            return DtoGas(
                co=ppm[self.__sensor.CO_GAS],
                h2=ppm[self.__sensor.H2_GAS],
                ch4=ppm[self.__sensor.CH4_GAS],
                lpg=ppm[self.__sensor.LPG_GAS],
                propane=ppm[self.__sensor.PROPANE_GAS],
                alcohol=ppm[self.__sensor.ALCOHOL_GAS],
                smoke=ppm[self.__sensor.SMOKE_GAS],
            )
        else:
            self.__logger.warning(msg="Failed get data from Gas Detection sensor")
            return None
