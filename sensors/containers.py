import logging.config
import os

from dependency_injector import containers, providers

from sensors.helpers.app_handlers import AppHandlers
from sensors.services.simple_sensors_service import SimpleSensorsService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_json(filepath=os.path.dirname(__file__) + "/config.json", required=True)

    logging = providers.Resource(logging.config.dictConfig, config=config.log())

    handlers = providers.Singleton(
        AppHandlers,
    )

    simple_sensors_service = providers.Factory(SimpleSensorsService)
