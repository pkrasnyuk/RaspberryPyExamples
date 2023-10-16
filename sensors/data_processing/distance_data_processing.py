import time
from typing import Optional
from sensors.data_processing.base_data_processing import BaseDataProcessing
from sensors.dto.dto_entity import DtoEntity
from sensors.dto.dto_lcd_messages import DtoLcdMessages
from sensors.services.distance_sensor_service import DistanceSensorService
from sensors.services.lcd_service import LCDService


class DistanceDataProcessing(BaseDataProcessing):
    def __init__(self, lcd_service: LCDService, distance_sensor_service: DistanceSensorService):
        self.__lcd_service: LCDService = lcd_service
        self.__distance_sensor_service: DistanceSensorService = distance_sensor_service
    
    def processing(self) -> None:
        self.__lcd_service.clear_messages()

        try:
            while True:
                distance_value: Optional[DtoEntity] = self.__distance_sensor_service.get_sensor_data()
                if distance_value is not None:
                    first_line_message: Optional[str] = f"Dist: {distance_value.distance:0.4f}m"
                    self.__lcd_service.send_messages(
                        messages=DtoLcdMessages(
                            first_line_message=first_line_message,
                        )
                    )
                time.sleep(10)
        except KeyboardInterrupt:
            pass
        finally:
            self.__lcd_service.clear_messages()
