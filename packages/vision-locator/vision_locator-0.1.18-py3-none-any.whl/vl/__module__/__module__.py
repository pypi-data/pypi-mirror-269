from typing import Callable, Dict
from ultralytics import YOLO
from vl.__module__.__config__ import __ModuleHorcrux


class Module(metaclass=__ModuleHorcrux):
    screenshot_method: Callable = None
    history_path: str = None
    device_resolution: dict = None
    windows_size: dict = None
    model: Dict[str, YOLO] = None
    max_detect_num: int = None
    conf_score: float = None
    timeout: int = None

    def load(screenshot_method: Callable,
             history_path: str,
             device_resolution: dict,
             windows_size: dict,
             model_path: str,
             max_detect_num: int,
             conf_score: float,
             timeout: int):
        '''
        Load configs
        '''
        ...

    def quit():
        '''
        Remove resources
        '''
        ...
