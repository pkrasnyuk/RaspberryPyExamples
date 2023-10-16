import logging.config
import os

from dependency_injector import containers, providers

from sensors.helpers.app_handlers import AppHandlers
from sensors.services.accelerometer_sensor_service import AccelerometerSensorService
from sensors.services.dht_sensor_service import DHTSensorService
from sensors.services.lcd_service import LCDService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_json(filepath=os.path.dirname(__file__) + "/config.json", required=True)

    logging = providers.Resource(logging.config.dictConfig, config=config.log())

    handlers = providers.Singleton(AppHandlers)

    lcd_service = providers.Factory(LCDService)
    dht_sensor_service = providers.Factory(DHTSensorService)
    accelerometer_sensor_service = providers.Factory(AccelerometerSensorService)
