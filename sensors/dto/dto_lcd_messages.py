from typing import Optional

from pydantic import Field

from sensors.dto.dto_entity import DtoEntity


class DtoLcdMessages(DtoEntity):
    first_line_message: Optional[str] = Field(default=None, max_length=16)
    second_line_message: Optional[str] = Field(default=None, max_length=16)
