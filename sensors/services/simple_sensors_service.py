import time
from signal import SIGINT, pause, signal

import Adafruit_DHT
from rpi_lcd import LCD

from sensors.services.sensors_service_interface import SensorsServiceInterface


class SimpleSensorsService(SensorsServiceInterface):
    def __init__(self):
        self.__dht_sensor = Adafruit_DHT.DHT11
        self.__lcd = LCD()

    def __handler(self, signal_received, frame) -> None:
        exit(0)

    def get_humidity_and_temperature(self, sersor_pin: int) -> None:

        while True:
            humidity, temperature = Adafruit_DHT.read_retry(sensor=self.__dht_sensor, pin=sersor_pin, delay_seconds=10)

            if humidity is not None and temperature is not None:
                print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
            else:
                print("Failed to retrieve data from humidity sensor")

    def set_lcd_message(self) -> None:

        signal(SIGINT, self.__handler)

        try:
            self.__lcd.text("Hello, ", 1)
            self.__lcd.text("Raspberry PI! ", 2)

            pause()
        except KeyboardInterrupt:
            pass
        finally:
            self.__lcd.clear()

    def set_humidity_and_temperature_as_lcd_messages(self, sersor_pin: int) -> None:

        signal(SIGINT, self.__handler)

        self.__lcd.clear()
        try:
            while True:
                humidity, temperature = Adafruit_DHT.read_retry(
                    sensor=self.__dht_sensor, pin=sersor_pin, delay_seconds=10
                )
                if humidity is not None and temperature is not None:
                    self.__lcd.text(f"Temp:      {temperature:0.1f}C", 1)
                    self.__lcd.text(f"Humidity:  {humidity:0.1f}%", 2)
                    time.sleep(10)
        except KeyboardInterrupt:
            pass
        finally:
            self.__lcd.clear()
