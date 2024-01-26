import json
import logging
from signal import SIGINT, signal

import click
from click_default_group import DefaultGroup
from dependency_injector.wiring import Provide, inject

from sensors.containers import Container
from sensors.helpers.app_handlers import AppHandlers
from sensors.services.lcd_service import LCDService
from sensors.services.mqtt_service import MQTTService
from sensors.services.scheduler_service import SchedulerService

log = logging.getLogger(f"{__name__}")


@click.command(name="services")
@inject
def services_task(
    scheduler_service: SchedulerService = Provide[Container.scheduler_service],
):
    scheduler_service.run()

    print("The sensors background scheduler is working. \r\n" "Press CTRL+C to quit.")
    while True:
        pass


@click.command(name="mqtt_example")
@inject
def mqtt_example_task(
    mqtt_service: MQTTService = Provide[Container.mqtt_service],
):
    mqtt_service.run()
    mqtt_service.send_message(message=json.dumps({"info": "test_message_303"}))
    mqtt_service.stop()


@click.command(name="default")
def default_task():
    pass


@click.group(cls=DefaultGroup, default="default", default_if_no_args=True)
@inject
def main(handlers: AppHandlers = Provide[Container.handlers]):
    handlers.init_global_handler()
    pass


main.add_command(services_task)
main.add_command(mqtt_example_task)
main.add_command(default_task)


def __handler(signal_received, frame, lcd_service: LCDService = Provide[Container.lcd_service]) -> None:
    lcd_service.clear_messages()
    print("done.")
    exit(0)


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    signal(SIGINT, __handler)
    main()
