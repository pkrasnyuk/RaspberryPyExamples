import logging
import subprocess
from typing import Optional

from rpi_lcd import LCD

from sensors.dto.dto_lcd_messages import DtoLcdMessages
from sensors.services.base_service import BaseService


class LCDService(BaseService):
    def __init__(self):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        p = subprocess.Popen(
            ["i2cget", "-y", "1", "0x27"],
            stdout=subprocess.PIPE,
        )
        status = str(p.stdout.readline())
        self.__lcd = None
        if status == "b'0x51\\n'":
            self.__lcd = LCD(address=0x27, width=16, rows=2, backlight=True)

    def send_messages(self, messages: Optional[DtoLcdMessages]) -> None:
        if self.__lcd is not None:
            try:
                if messages is not None:
                    if messages.first_line_message is not None:
                        self.__lcd.text(messages.first_line_message, 1)
                    if messages.second_line_message is not None:
                        self.__lcd.text(messages.second_line_message, 2)
            except Exception as ex:
                self.__logger.exception(f"Can not send lcd messages because of exception: {ex}")
                pass
        else:
            self.__logger.warning(msg="Failed for initialise LCD display")
            pass

    def clear_messages(self) -> None:
        if self.__lcd is not None:
            self.__lcd.clear()
