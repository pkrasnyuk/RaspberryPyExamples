import logging
from sensors.containers import Container
from sensors.helpers.app_handlers import AppHandlers
from sensors.helpers.simple_helpers import get_humidity_and_temperature

log = logging.getLogger(f"{__name__}")


DHT_PIN = 19

def main(handlers: AppHandlers):
    handlers.init_global_handler()

    get_humidity_and_temperature(sersor_pin=DHT_PIN)


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    
    main(handlers=container.handlers())
