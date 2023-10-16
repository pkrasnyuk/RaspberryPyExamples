import time
from typing import Optional

from sensors.data_processing.base_data_processing import BaseDataProcessing
from sensors.dto.dto_accelerometry import DtoAccelerometry
from sensors.services.accelerometer_sensor_service import AccelerometerSensorService


class AccelerometerDataProcessing(BaseDataProcessing):
    def __init__(self, accelerometer_sensor_service: AccelerometerSensorService):
        self.__accelerometer_sensor_service: AccelerometerSensorService = accelerometer_sensor_service

    def processing(self) -> None:
        try:
            while True:
                accelerometry_data: Optional[DtoAccelerometry] = self.__accelerometer_sensor_service.get_sensor_data()
                if accelerometry_data is not None:
                    print("Acceleration:")
                    print(f"    X: {accelerometry_data.x_acceleration:.3f} m/s^2")
                    print(f"    Y: {accelerometry_data.y_acceleration:.3f} m/s^2")
                    print(f"    Z: {accelerometry_data.z_acceleration:.3f} m/s^2")

                    print("Raw:")
                    print(f"    X: {accelerometry_data.x_raw:.3f}")
                    print(f"    Y: {accelerometry_data.y_raw:.3f}")
                    print(f"    Z: {accelerometry_data.z_raw:.3f}")

                    print("Calibrated offsets:")
                    print(f"    X: {accelerometry_data.x_offset:.3f}")
                    print(f"    Y: {accelerometry_data.y_offset:.3f}")
                    print(f"    Z: {accelerometry_data.z_offset:.3f}")

                    print(f"Dropped: {accelerometry_data.dropped}")
                    print(f"Tapped: {accelerometry_data.tapped}")
                    print(f"Motion detected: {accelerometry_data.motion_detected}")

                time.sleep(1)
        except KeyboardInterrupt:
            pass
