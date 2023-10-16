import logging

import click
from click_default_group import DefaultGroup
from dependency_injector.wiring import Provide, inject

from sensors.containers import Container
from sensors.data_processing.accelerometer_data_processing import AccelerometerDataProcessing
from sensors.data_processing.base_data_processing import BaseDataProcessing
from sensors.data_processing.wheather_data_processing import WheatherDataProcessing
from sensors.helpers.app_handlers import AppHandlers
from sensors.services.accelerometer_sensor_service import AccelerometerSensorService
from sensors.services.dht_sensor_service import DHTSensorService
from sensors.services.lcd_service import LCDService

log = logging.getLogger(f"{__name__}")

DHT_PIN = 19


@click.command(name="wheather")
@inject
def wheather_task(
    lcd_service: LCDService = Provide[Container.lcd_service],
    dht_sensor_service: DHTSensorService = Provide[Container.dht_sensor_service],
):
    dht_sensor_service.set_sersor_pin(pin=DHT_PIN)

    wheather_data_processing: BaseDataProcessing = WheatherDataProcessing(
        lcd_service=lcd_service, dht_sensor_service=dht_sensor_service
    )
    wheather_data_processing.processing()


@click.command(name="accelerometry")
@inject
def accelerometry_task(
    accelerometer_sensor_service: AccelerometerSensorService = Provide[Container.accelerometer_sensor_service],
):
    accelerometer_data_processing: BaseDataProcessing = AccelerometerDataProcessing(
        accelerometer_sensor_service=accelerometer_sensor_service
    )
    accelerometer_data_processing.processing()


@click.group(cls=DefaultGroup, default="default", default_if_no_args=True)
@inject
def main(handlers: AppHandlers = Provide[Container.handlers]):
    handlers.init_global_handler()
    pass


@click.command(name="default")
def default_task():
    pass


main.add_command(wheather_task)
main.add_command(accelerometry_task)
main.add_command(default_task)


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main()
