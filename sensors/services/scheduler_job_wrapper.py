from sensors.data_processing.base_data_processing import BaseDataProcessing
from sensors.dto.dto_scheduler_job import DtoSchedulerJob


class SchedulerJobWrapper:
    def __init__(self, job: DtoSchedulerJob, data_processing: BaseDataProcessing):
        self.__job = job
        self.__data_processing = data_processing
    
    def get_job_info(self):
        return self.__job

    def execute_scheduler_job(self):
        if self.__data_processing is not None:
            self.__data_processing.processing()
