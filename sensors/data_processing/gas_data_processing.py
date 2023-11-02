import time
from typing import Optional

from sensors.data_processing.base_data_processing import BaseDataProcessing
from sensors.dto.dto_gas import DtoGas
from sensors.dto.dto_lcd_messages import DtoLcdMessages
from sensors.services.gas_sensor_service import GazSensorService
from sensors.services.lcd_service import LCDService


class GazDataProcessing(BaseDataProcessing):
    def __init__(self, lcd_service: LCDService, gas_sensor_service: GazSensorService):
        self.__lcd_service: LCDService = lcd_service
        self.__gas_sensor_service: GazSensorService = gas_sensor_service

    def processing(self) -> None:
        self.__lcd_service.clear_messages()
        first_line_message: Optional[str] = ""
        second_line_message: Optional[str] = ""

        gas_detection_value: Optional[DtoGas] = self.__gas_sensor_service.get_sensor_data()
        if gas_detection_value is not None:
            if gas_detection_value.co is not None:
                co_value: float = gas_detection_value.co * 100.0
                first_line_message = f"CO: {co_value:0.2f}%"
            if gas_detection_value.h2 is not None:
                h2_value: float = gas_detection_value.h2 * 100.0
                second_line_message = f"H2: {h2_value:0.2f}%"
            self.__lcd_service.send_messages(
                messages=DtoLcdMessages(
                    first_line_message=first_line_message,
                    second_line_message=second_line_message,
                )
            )
            time.sleep(15)
            if gas_detection_value.ch4 is not None:
                ch4_value: float = gas_detection_value.ch4 * 100.0
                first_line_message = f"CH4: {ch4_value:0.2f}%"
            if gas_detection_value.lpg is not None:
                lpg_value: float = gas_detection_value.lpg * 100.0
                second_line_message = f"LPG: {lpg_value:0.2f}%"
            self.__lcd_service.send_messages(
                messages=DtoLcdMessages(
                    first_line_message=first_line_message,
                    second_line_message=second_line_message,
                )
            )
            time.sleep(15)
            if gas_detection_value.propane is not None:
                propane_value: float = gas_detection_value.propane * 100.0
                first_line_message = f"Propane: {propane_value:0.2f}%"
            if gas_detection_value.alcohol is not None:
                alcohol_value: float = gas_detection_value.alcohol * 100.0
                second_line_message = f"Alcohol: {alcohol_value:0.2f}%"
            self.__lcd_service.send_messages(
                messages=DtoLcdMessages(
                    first_line_message=first_line_message,
                    second_line_message=second_line_message,
                )
            )
            time.sleep(15)
            if gas_detection_value.smoke is not None:
                smoke_value: float = gas_detection_value.smoke * 100.0
                first_line_message = f"Smoke: {smoke_value:0.2f}%"
            second_line_message = ""
            self.__lcd_service.send_messages(
                messages=DtoLcdMessages(
                    first_line_message=first_line_message,
                    second_line_message=second_line_message,
                )
            )
