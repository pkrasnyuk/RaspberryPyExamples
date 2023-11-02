from typing import Optional

from sensors.data_processing.base_data_processing import BaseDataProcessing
from sensors.dto.dto_lcd_messages import DtoLcdMessages
from sensors.dto.dto_weather import DtoWeather
from sensors.services.dht_sensor_service import DHTSensorService
from sensors.services.influx_db_service import InfluxDbService
from sensors.services.lcd_service import LCDService


class WeatherDataProcessing(BaseDataProcessing):
    def __init__(
        self,
        lcd_service: LCDService,
        dht_sensor_service: DHTSensorService,
        influx_db_service: InfluxDbService,
        weather_bucket: str,
    ):
        self.__lcd_service: LCDService = lcd_service
        self.__dht_sensor_service: DHTSensorService = dht_sensor_service
        self.__influx_db_service: InfluxDbService = influx_db_service
        self.__weather_bucket: str = weather_bucket

    def processing(self) -> None:
        self.__lcd_service.clear_messages()

        weather_data: Optional[DtoWeather] = self.__dht_sensor_service.get_sensor_data()
        if weather_data is not None:
            first_line_message: Optional[str] = (
                f"Temp:      {weather_data.temperature:0.1f}C" if weather_data.temperature is not None else None
            )
            second_line_message: Optional[str] = (
                f"Humidity:  {weather_data.humidity:0.1f}%" if weather_data.humidity is not None else None
            )
            self.__lcd_service.send_messages(
                messages=DtoLcdMessages(first_line_message=first_line_message, second_line_message=second_line_message)
            )
            self.__influx_db_service.save_point(
                bucket_name=self.__weather_bucket, measurement_name="weather", model=weather_data
            )
