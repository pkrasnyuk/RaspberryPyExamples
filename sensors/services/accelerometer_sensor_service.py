import logging
from typing import Optional

import adafruit_adxl34x
import board
import busio

from sensors.dto.dto_accelerometry import DtoAccelerometry
from sensors.services.base_sensor_service import BaseSensorService


class AccelerometerSensorService(BaseSensorService):
    def __init__(self):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__i2c = busio.I2C(board.SCL, board.SDA)
        if self.__i2c is not None:
            self.__sensor = adafruit_adxl34x.ADXL345(self.__i2c)
            if self.__sensor is not None:
                self.__sensor.enable_freefall_detection(threshold=10, time=25)
                self.__sensor.enable_motion_detection(threshold=18)
                self.__sensor.enable_tap_detection(tap_count=1, threshold=20, duration=50, latency=20, window=255)
            else:
                self.__logger.warning(msg="Failed to initialize Accelerometer Sensor")
        else:
            self.__logger.warning(msg="Failed to initialize I2C connection")

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

        if self.__sensor is not None:
            (x_acceleration, y_acceleration, z_acceleration) = self.__sensor.acceleration
            x_raw = self.__sensor.raw_x
            y_raw = self.__sensor.raw_y
            z_raw = self.__sensor.raw_z
            x_offset = round(-1 * x_raw / 8)
            y_offset = round(-1 * y_raw / 8)
            z_offset = round(-1 * (z_raw - 250) / 8)
            dropped = self.__sensor.events["freefall"]
            tapped = self.__sensor.events["tap"]
            motion_detected = self.__sensor.events["motion"]

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
                motion_detected=motion_detected,
            )
        else:
            self.__logger.warning(msg="Failed to retrieve data from accelerometer sensor")
            return None
