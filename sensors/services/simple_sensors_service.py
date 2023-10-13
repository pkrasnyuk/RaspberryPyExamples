import Adafruit_DHT

from sensors.services.sensors_service_interface import SensorsServiceInterface


class SimpleSensorsService(SensorsServiceInterface):
    def __init__(self):
        self.__dht_sensor = Adafruit_DHT.DHT11

    def get_humidity_and_temperature(self, sersor_pin: int) -> None:

        while True:
            humidity, temperature = Adafruit_DHT.read_retry(sensor=self.__dht_sensor, pin=sersor_pin, delay_seconds=10)

            if humidity is not None and temperature is not None:
                print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
            else:
                print("Failed to retrieve data from humidity sensor")
