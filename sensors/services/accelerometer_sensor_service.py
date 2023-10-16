import logging
from typing import Optional
from sensors.dto.dto_accelerometry import DtoAccelerometry
from sensors.services.base_sensor_service import BaseSensorService

import board
import busio
import adafruit_adxl34x


class AccelerometerSensorService(BaseSensorService):
    def __init__(self):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__i2c = busio.I2C(board.SCL, board.SDA)
        self.__accelerometer = adafruit_adxl34x.ADXL345(self.__i2c)
        self.__accelerometer.enable_freefall_detection(threshold=10, time=25)
        self.__accelerometer.enable_motion_detection(threshold=18)
        self.__accelerometer.enable_tap_detection(tap_count=1, threshold=20, duration=50, latency=20, window=255)

    def get_sensor_data(self) -> Optional[DtoAccelerometry]:

        x_acceleration: float = 0.0
        y_acceleration: float = 0.0
        z_acceleration: float = 0.0
        x_raw: float = 0.0
        y_raw: float = 0.0
        z_raw: float = 0.0
        x_offset: float = 0.0
        y_offset: float = 0.0
        z_offset: float = 0.0
        dropped: Optional[bool] = None
        tapped: Optional[bool] = None
        motion_detected: Optional[bool] = None

        if self.__accelerometer is not None:
            (x_acceleration, y_acceleration, z_acceleration) = self.__accelerometer.acceleration
            x_raw = self.__accelerometer.raw_x
            y_raw = self.__accelerometer.raw_y
            z_raw = self.__accelerometer.raw_z
            x_offset = round(-1 * x_raw / 8)
            y_offset = round(-1 * y_raw / 8)
            z_offset = round(-1 * (z_raw - 250) / 8)
            dropped = self.__accelerometer.events["freefall"]
            tapped = self.__accelerometer.events["tap"]
            motion_detected = self.__accelerometer.events["motion"]

            return DtoAccelerometry(
                x_acceleration=x_acceleration,
                y_acceleration=y_acceleration,
                z_acceleration=z_acceleration,
                x_raw=x_raw,
                y_raw=y_raw,
                z_raw=z_raw,
                x_offset=x_offset,
                y_offset=y_offset,
                z_offset=z_offset,
                dropped=dropped,
                tapped=tapped,
                motion_detected=motion_detected
            )
        else:
            self.__logger.warning(msg="Failed to retrieve data from accelerometer sensor")
            return None
