import logging

from dependency_injector.wiring import Provide, inject

from sensors.containers import Container
from sensors.data_processing.base_data_processing import BaseDataProcessing
from sensors.data_processing.wheather_data_processing import WheatherDataProcessing
from sensors.helpers.app_handlers import AppHandlers
from sensors.services.dht_sensor_service import DHTSensorService
from sensors.services.lcd_service import LCDService

log = logging.getLogger(f"{__name__}")

DHT_PIN = 19


@inject
def main(
    handlers: AppHandlers = Provide[Container.handlers],
    lcd_service: LCDService = Provide[Container.lcd_service],
    dht_sensor_service: DHTSensorService = Provide[Container.dht_sensor_service],
):
    handlers.init_global_handler()

    dht_sensor_service.set_sersor_pin(pin=DHT_PIN)

    wheather_data_processing: BaseDataProcessing = WheatherDataProcessing(
        lcd_service=lcd_service, dht_sensor_service=dht_sensor_service
    )
    wheather_data_processing.processing()


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main()
