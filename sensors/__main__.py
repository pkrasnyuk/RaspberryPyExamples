import logging

from sensors.containers import Container
from sensors.helpers.app_handlers import AppHandlers
from sensors.services.sensors_service_interface import SensorsServiceInterface

log = logging.getLogger(f"{__name__}")


DHT_PIN = 19


def main(handlers: AppHandlers, sensors_service_interface: SensorsServiceInterface):
    handlers.init_global_handler()
    sensors_service_interface.set_humidity_and_temperature_as_lcd_messages(sersor_pin=DHT_PIN)


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main(handlers=container.handlers(), sensors_service_interface=container.simple_sensors_service())
