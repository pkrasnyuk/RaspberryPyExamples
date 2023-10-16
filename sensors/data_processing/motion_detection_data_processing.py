import time
from typing import Optional
from sensors.data_processing.base_data_processing import BaseDataProcessing
from sensors.dto.dto_lcd_messages import DtoLcdMessages
from sensors.dto.dto_motion import DtoMotion
from sensors.services.lcd_service import LCDService
from sensors.services.motion_detection_sensor_service import MotionDetectionSensorService


class MotionDetectionDataProcessing(BaseDataProcessing):
    def __init__(self, lcd_service: LCDService, motion_detection_sensor_service: MotionDetectionSensorService):
        self.__lcd_service: LCDService = lcd_service
        self.__motion_detection_sensor_service: MotionDetectionSensorService = motion_detection_sensor_service

    def processing(self) -> None:
        self.__lcd_service.clear_messages()
        first_line_message: Optional[str] = ""

        try:
            old_motion_detection_value: Optional[DtoMotion] = self.__motion_detection_sensor_service.get_sensor_data()
            while True:
                motion_detection_value: Optional[DtoMotion] = self.__motion_detection_sensor_service.get_sensor_data()
                if motion_detection_value is not None:
                    if motion_detection_value.motion_detection:
                        if old_motion_detection_value is not None and not old_motion_detection_value.motion_detection:
                            first_line_message = "Motion detected!"
                    else:
                        if old_motion_detection_value is not None and old_motion_detection_value.motion_detection:
                            first_line_message = "Motion ended!"
                    self.__lcd_service.send_messages(
                        messages=DtoLcdMessages(first_line_message=first_line_message)
                    )
                old_motion_detection_value = motion_detection_value
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.__lcd_service.clear_messages()
