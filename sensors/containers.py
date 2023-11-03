import logging.config
import os
from typing import List, Optional

from dependency_injector import containers, providers

from sensors.data_processing.accelerometer_data_processing import AccelerometerDataProcessing
from sensors.data_processing.distance_data_processing import DistanceDataProcessing
from sensors.data_processing.gas_data_processing import GazDataProcessing
from sensors.data_processing.motion_detection_data_processing import MotionDetectionDataProcessing
from sensors.data_processing.weather_data_processing import WeatherDataProcessing
from sensors.dto.dto_scheduler_job import DtoSchedulerJob
from sensors.dto.dto_sensor import DtoSensor
from sensors.helpers.app_handlers import AppHandlers
from sensors.services.accelerometer_sensor_service import AccelerometerSensorService
from sensors.services.dht_sensor_service import DHTSensorService
from sensors.services.distance_sensor_service import DistanceSensorService
from sensors.services.gas_sensor_service import GazSensorService
from sensors.services.influx_db_service import InfluxDbService
from sensors.services.lcd_service import LCDService
from sensors.services.motion_detection_sensor_service import MotionDetectionSensorService
from sensors.services.scheduler_job_wrapper import SchedulerJobWrapper
from sensors.services.scheduler_service import SchedulerService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_json(filepath=os.path.dirname(__file__) + "/config.json", required=True)

    logging = providers.Resource(logging.config.dictConfig, config=config.log())

    handlers = providers.Singleton(AppHandlers)

    influxdb_config = config.influxdb()
    influx_db_service = providers.Factory(
        InfluxDbService,
        url=influxdb_config["url"],
        token=influxdb_config["token"],
        org=influxdb_config["org"],
    )

    lcd_service = providers.Factory(LCDService)

    scheduler_job_wrapper_providers_list = providers.List()
    services = config.services()
    if services is not None and len(services) > 0:
        for service in services:
            service_sensors: Optional[List[DtoSensor]] = []
            if "sensors" in service and len(service["sensors"]) > 0:
                service_sensors = []
                for sensor in service["sensors"]:
                    service_sensors.append(DtoSensor(name=sensor["name"], pin=sensor["pin"]))
            else:
                service_sensors = None
            scheduler_job = DtoSchedulerJob(
                name=service["name"] if "name" in service else None,
                sensors=service_sensors,
                cron=service["cron"] if "cron" in service and service["cron"] != "" else None,
            )
            cron: Optional[str] = scheduler_job.get_crontab()
            if cron is not None:
                sensors: Optional[List[DtoSensor]] = scheduler_job.get_sensors()
                if scheduler_job.get_name() == "weather" and sensors is not None and len(sensors) > 0:
                    dht_sensor: Optional[DtoSensor] = next((x for x in sensors if x.get_name() == "DHT"), None)
                    if dht_sensor is not None:
                        dht_sensor_pin: Optional[int] = dht_sensor.get_pin()
                        if dht_sensor_pin is not None:
                            dht_sensor_service = providers.Factory(
                                DHTSensorService,
                                pin=dht_sensor_pin,
                            )
                            weather_data_processing = providers.Factory(
                                WeatherDataProcessing,
                                lcd_service=lcd_service,
                                dht_sensor_service=dht_sensor_service,
                                influx_db_service=influx_db_service,
                                weather_bucket=influxdb_config["dht_bucket"],
                            )
                            weather_wrapper = providers.Factory(
                                SchedulerJobWrapper,
                                job=scheduler_job,
                                data_processing=weather_data_processing,
                            )
                            scheduler_job_wrapper_providers_list.add_args(weather_wrapper)
                if scheduler_job.get_name() == "accelerometry":
                    accelerometer_sensor_service = providers.Factory(AccelerometerSensorService)
                    accelerometer_data_processing = providers.Factory(
                        AccelerometerDataProcessing,
                        accelerometer_sensor_service=accelerometer_sensor_service,
                    )
                    accelerometer_wrapper = providers.Factory(
                        SchedulerJobWrapper,
                        job=scheduler_job,
                        data_processing=accelerometer_data_processing,
                    )
                    scheduler_job_wrapper_providers_list.add_args(accelerometer_wrapper)
                if scheduler_job.get_name() == "motion_detection" and sensors is not None and len(sensors) > 0:
                    pir_sensor: Optional[DtoSensor] = next((x for x in sensors if x.get_name() == "PIR"), None)
                    if pir_sensor is not None:
                        pir_sensor_pin: Optional[int] = pir_sensor.get_pin()
                        if pir_sensor_pin is not None:
                            motion_detection_sensor_service = providers.Factory(
                                MotionDetectionSensorService,
                                pin=pir_sensor_pin,
                            )
                            motion_detection_data_processing = providers.Factory(
                                MotionDetectionDataProcessing,
                                lcd_service=lcd_service,
                                motion_detection_sensor_service=motion_detection_sensor_service,
                            )
                            motion_detection_wrapper = providers.Factory(
                                SchedulerJobWrapper,
                                job=scheduler_job,
                                data_processing=motion_detection_data_processing,
                            )
                            scheduler_job_wrapper_providers_list.add_args(motion_detection_wrapper)
                if scheduler_job.get_name() == "gaz_detection" and sensors is not None and len(sensors) > 0:
                    mq2_sensor: Optional[DtoSensor] = next((x for x in sensors if x.get_name() == "MQ2"), None)
                    if mq2_sensor is not None:
                        mq2_sensor_pin: Optional[int] = mq2_sensor.get_pin()
                        if mq2_sensor_pin is not None:
                            gas_sensor_service = providers.Factory(
                                GazSensorService,
                                pin=mq2_sensor_pin,
                            )
                            gaz_detection_data_processing = providers.Factory(
                                GazDataProcessing,
                                lcd_service=lcd_service,
                                gas_sensor_service=gas_sensor_service,
                            )
                            gaz_detection_wrapper = providers.Factory(
                                SchedulerJobWrapper,
                                job=scheduler_job,
                                data_processing=gaz_detection_data_processing,
                            )
                            scheduler_job_wrapper_providers_list.add_args(gaz_detection_wrapper)
                if scheduler_job.get_name() == "distance" and sensors is not None and len(sensors) > 1:
                    hc_sr04_f_sensor: Optional[DtoSensor] = next(
                        (x for x in sensors if x.get_name() == "HC_SR04_F"), None
                    )
                    hc_sr04_s_sensor: Optional[DtoSensor] = next(
                        (x for x in sensors if x.get_name() == "HC_SR04_S"), None
                    )
                    if hc_sr04_f_sensor is not None and hc_sr04_s_sensor is not None:
                        hc_sr04_f_sensor_pin_f: Optional[int] = hc_sr04_f_sensor.get_pin()
                        hc_sr04_s_sensor_pin_s: Optional[int] = hc_sr04_s_sensor.get_pin()
                        if hc_sr04_f_sensor_pin_f is not None and hc_sr04_s_sensor_pin_s is not None:
                            distance_sensor_service = providers.Factory(
                                DistanceSensorService,
                                pin=hc_sr04_f_sensor_pin_f,
                                sub_pin=hc_sr04_s_sensor_pin_s,
                            )
                            distance_data_processing = providers.Factory(
                                DistanceDataProcessing,
                                lcd_service=lcd_service,
                                distance_sensor_service=distance_sensor_service,
                            )
                            distance_wrapper = providers.Factory(
                                SchedulerJobWrapper,
                                job=scheduler_job,
                                data_processing=distance_data_processing,
                            )
                            scheduler_job_wrapper_providers_list.add_args(distance_wrapper)

    scheduler_service = providers.Factory(SchedulerService, scheduler_job_wrappers=scheduler_job_wrapper_providers_list)
