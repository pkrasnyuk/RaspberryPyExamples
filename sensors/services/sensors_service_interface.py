class SensorsServiceInterface:
    def get_humidity_and_temperature(self, sersor_pin: int) -> None:
        pass

    def set_lcd_message(self) -> None:
        pass

    def set_humidity_and_temperature_as_lcd_messages(self, sersor_pin: int) -> None:
        pass
