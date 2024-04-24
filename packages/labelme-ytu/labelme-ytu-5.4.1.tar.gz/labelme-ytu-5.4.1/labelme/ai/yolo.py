import os
from os.path import exists
from urllib.parse import urlparse

from labelme.widgets import ErrorDialog

import sys 

#ultralytics gives error if stdout is None
if(sys.stdout is None):
    f = open(os.devnull, 'w')
    sys.stdout = f

from ultralytics import YOLO

class Yolo:
    model_path = ""

    def __init__(self, model_path):
        self.model_path = model_path

    @staticmethod
    def getUniqueName(path):
        parent_folder = os.path.basename(os.path.dirname(path))
        file_name = os.path.basename(path)
        return f"{parent_folder}/{file_name}"

    @staticmethod
    def getFileName(path):
        return os.path.basename(path)

    def setModel(self, path):
        self.model_path = path

    def getResults(self, image_paths):
        
        if(not self.model_path.lower().endswith(".pt")):
            msgBox = ErrorDialog("Could not run the model.\nCheck model path in AI -> Object Detection Model.")
            msgBox.show()
            return None
        
        model = YOLO(self.model_path)
        return model(image_paths)



    
