import logging

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from sensors.dto.dto_entity import DtoEntity
from sensors.services.base_service import BaseService


class InfluxDbService(BaseService):
    def __init__(self, url: str, token: str, org: str):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__org = org
        self.__client = InfluxDBClient(url=url, token=token, org=self.__org)
        self.__buckets_api = self.__client.buckets_api()
        self.__write_api = self.__client.write_api(write_options=SYNCHRONOUS)

    def save_point(self, bucket_name: str, measurement_name: str, model: DtoEntity) -> None:
        try:
            bucket = self.__buckets_api.find_bucket_by_name(bucket_name=bucket_name)
            if bucket is None:
                bucket = self.__buckets_api.create_bucket(bucket_name=bucket_name, org=self.__org)

            if bucket is not None and model is not None:
                point = Point(measurement_name=measurement_name).tag(key="location", value="localhost")
                point._fields = model.model_dump()
                self.__write_api.write(bucket=bucket_name, org=self.__org, record=point)
            else:
                self.__logger.warning(msg="Failed to save point to InfluxDb")
        except Exception as ex:
            self.__logger.exception(f"Can not save point to InfluxDb because of exception: {ex}")
            pass

        return None
