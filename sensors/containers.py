import os
import logging.config
from dependency_injector import containers, providers

from sensors.helpers.app_handlers import AppHandlers

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_json(filepath=os.path.dirname(__file__) + "/config.json", required=True)

    logging = providers.Resource(logging.config.dictConfig, config=config.log())

    handlers = providers.Singleton(
        AppHandlers,
    )