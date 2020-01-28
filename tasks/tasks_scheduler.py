from tasks.task_executor_itf import ITaskExecutor

from tasks.SAUVC.gate.task_executor.gate_task_executor import GateTaskExecutor as GateExecutor
from tasks.SAUVC.buckets.task_executor.buckets_task_executor import BucketTaskExecutor

class TaskSchedululer(ITaskExecutor):

    def __init__(self, control_dict, sensors_dict, camera_client, main_logger):
        """
        @param: movement_object is an object of Movements Class
            keywords: movements; torpedoes; manipulator;
        @param: sensors_dict is a dictionary of references to sensors objects
            keywords: ahrs; depth; hydrophones; distance;
        @param: camera_client 
        @param: main_logger is a reference to logger of main thread
        """
        self.control_dict = control_dict
        self.sensors_dict = sensors_dict
        self.camera_client = camera_client
        self.logger = main_logger

    def run(self):
        """
        This method is started by main object.
        """
        self.logger.log("Task scheduler is running")

        gate_executor = GateExecutor(self.control_dict['movements'], self.sensors_dict,
                                     self.camera_client, self.logger)
        gate_executor.run()

        self.logger.log("Gate finshed")

        bucket_executor = BucketTaskExecutor(self.control_dict['movements'], self.sensors_dict,
                                     self.camera_client, self.logger)
        bucket_executor.run()

        self.logger.log("Buckets finished")