import logging

import click
from click_default_group import DefaultGroup
from dependency_injector.wiring import Provide, inject

from sensors.containers import Container
from sensors.data_processing.accelerometer_data_processing import AccelerometerDataProcessing
from sensors.data_processing.base_data_processing import BaseDataProcessing
from sensors.data_processing.gas_data_processing import GazDataProcessing
from sensors.data_processing.motion_detection_data_processing import MotionDetectionDataProcessing
from sensors.data_processing.wheather_data_processing import WheatherDataProcessing
from sensors.helpers.app_handlers import AppHandlers
from sensors.services.accelerometer_sensor_service import AccelerometerSensorService
from sensors.services.dht_sensor_service import DHTSensorService
from sensors.services.gas_sensor_service import GazSensorService
from sensors.services.lcd_service import LCDService
from sensors.services.motion_detection_sensor_service import MotionDetectionSensorService

log = logging.getLogger(f"{__name__}")


@click.command(name="wheather")
@inject
def wheather_task(
    lcd_service: LCDService = Provide[Container.lcd_service],
    dht_sensor_service: DHTSensorService = Provide[Container.dht_sensor_service],
):
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


@click.command(name="motion_detection")
@inject
def motion_detection_task(
    lcd_service: LCDService = Provide[Container.lcd_service],
    motion_detection_sensor_service: MotionDetectionSensorService = Provide[Container.motion_detection_sensor_service],
):
    motion_detection_data_processing: BaseDataProcessing = MotionDetectionDataProcessing(
        lcd_service=lcd_service, motion_detection_sensor_service=motion_detection_sensor_service
    )
    motion_detection_data_processing.processing()


@click.command(name="gaz_detection")
@inject
def gaz_detection_task(
    lcd_service: LCDService = Provide[Container.lcd_service],
    gas_sensor_service: GazSensorService = Provide[Container.gas_sensor_service],
):
    gaz_data_processing: BaseDataProcessing = GazDataProcessing(
        lcd_service=lcd_service, gas_sensor_service=gas_sensor_service
    )
    gaz_data_processing.processing()


@click.command(name="default")
def default_task():
    pass


@click.group(cls=DefaultGroup, default="default", default_if_no_args=True)
@inject
def main(handlers: AppHandlers = Provide[Container.handlers]):
    handlers.init_global_handler()
    pass


main.add_command(wheather_task)
main.add_command(accelerometry_task)
main.add_command(motion_detection_task)
main.add_command(gaz_detection_task)
main.add_command(default_task)


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main()
