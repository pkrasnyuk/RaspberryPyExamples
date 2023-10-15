import time
from typing import Optional
from sensors.data_processing.base_data_processing import BaseDataProcessing
from sensors.dto.dto_lcd_messages import DtoLcdMessages
from sensors.dto.dto_weather import DtoWeather
from sensors.services.base_service import BaseService
from sensors.services.dht_sensor_service import DHTSensorService
from sensors.services.lcd_service import LCDService


class WheatherDataProcessing(BaseDataProcessing):
    def __init__(self, lcd_service: LCDService, dht_sensor_service: DHTSensorService):
        self.__lcd_service: LCDService = lcd_service
        self.__dht_sensor_service: DHTSensorService = dht_sensor_service

    def processing(self) -> None:
        self.__lcd_service.clear_messages()

        try:
            while True:
                wheather_data: Optional[DtoWeather] = (
                    self.__dht_sensor_service.get_sensor_data()
                )
                if wheather_data is not None:
                    first_line_message: Optional[str] = (
                        f"Temp:      {wheather_data.temperature:0.1f}C" if wheather_data.temperature is not None else None
                    )
                    second_line_message: Optional[str] = (
                        f"Humidity:  {wheather_data.humidity:0.1f}%" if wheather_data.humidity is not None else None
                    )
                    self.__lcd_service.send_messages(
                        messages=DtoLcdMessages(first_line_message=first_line_message, second_line_message=second_line_message)
                    )
                time.sleep(10)
        except KeyboardInterrupt:
            pass
        finally:
            self.__lcd_service.clear_messages()
