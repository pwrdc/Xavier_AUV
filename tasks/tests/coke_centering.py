from tasks.task_executor_itf import ITaskExecutor
from neural_networks.DarknetClient import DarknetClient
from communication.rpi_broker.movements import Movements
from utils.stopwatch import Stopwatch
from utils.centering import center_rov
from configs.config import get_config
from time import sleep
from definitions import IP_ADDRESS, DARKNET_PORT

class CokeCenteringTest(ITaskExecutor):
    def __init__(self,control_dict: Movements, sensors_dict,
                camera_client, main_logger):
        self._control = control_dict['movements']
        self.depth_sensor = sensors_dict['depth']
        self._logger = main_logger
        self._control.pid_turn_on()
        self._control.pid_set_depth(0.3)
        self.darknet_client = DarknetClient()
        self._logger.log("Coke centering test started")
    
    def run(self):
        self.darknet_client.load_model('coke')
        self._logger.log("Coke model loaded")
        bbox = False
        while not bbox:
            bbox = self.darknet_client.predict()[0].normalize(480, 480) #TODO
            sleep(0.1)
        self._logger.log("out of predicting loop")
        #bbox.normalize()
        position_x = bbox.x      #TO DO - returning bbox instead of list
        position_y = bbox.y

        self._logger.log("poz: x="+str(position_x)+" y="+str(position_y))

        while abs(position_x) > 0.2 and abs(position_y) > 0.2:
            self._logger.log("in ceentring")
            bbox = self.darknet_client.predict()[0].normalize(480, 480)
            if bbox:
                sleep(0.1)
                #bbox.normalize()
                position_x = bbox.x      #TO DO - returning bbox instead of list
                position_y = bbox.y
                self._logger.log("pos: x="+str(position_x)+" y="+str(position_y))
                
                center_rov(move = self._control,Bbox = bbox, depth_sensor = self.depth_sensor)


    