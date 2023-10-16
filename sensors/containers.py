import logging.config
import os

from dependency_injector import containers, providers

from sensors.helpers.app_handlers import AppHandlers
from sensors.services.accelerometer_sensor_service import AccelerometerSensorService
from sensors.services.dht_sensor_service import DHTSensorService
from sensors.services.distance_sensor_service import DistanceSensorService
from sensors.services.gas_sensor_service import GazSensorService
from sensors.services.lcd_service import LCDService
from sensors.services.motion_detection_sensor_service import MotionDetectionSensorService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_json(filepath=os.path.dirname(__file__) + "/config.json", required=True)

    logging = providers.Resource(logging.config.dictConfig, config=config.log())

    handlers = providers.Singleton(AppHandlers)

    lcd_service = providers.Factory(LCDService)
    dht_sensor_service = providers.Factory(DHTSensorService, pin=config.DHT_PIN())
    accelerometer_sensor_service = providers.Factory(AccelerometerSensorService)
    motion_detection_sensor_service = providers.Factory(MotionDetectionSensorService, pin=config.PIR_PIN())
    gas_sensor_service = providers.Factory(GazSensorService, pin=config.MQ2_PIN())
    distance_sensor_service = providers.Factory(
        DistanceSensorService, pin=config.HC_SR04_PIN(), sub_pin=config.HC_SR04_SUB_PIN()
    )
