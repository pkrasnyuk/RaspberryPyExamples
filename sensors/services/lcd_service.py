import logging
from typing import Optional

from rpi_lcd import LCD

from sensors.dto.dto_lcd_messages import DtoLcdMessages
from sensors.services.base_service import BaseService


class LCDService(BaseService):
    def __init__(self):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__lcd = LCD()

    def send_messages(self, messages: Optional[DtoLcdMessages]) -> None:
        try:
            if messages is not None:
                if messages.first_line_message is not None:
                    self.__lcd.text(messages.first_line_message, 1)
                if messages.second_line_message is not None:
                    self.__lcd.text(messages.second_line_message, 2)
        except Exception as ex:
            self.__logger.exception(f"Can not send lcd messages because of exception: {ex}")
            pass

    def clear_messages(self) -> None:
        self.__lcd.clear()
