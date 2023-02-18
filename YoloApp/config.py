import os


class Config:
    def __init__(self):
        self.BASE_PATH = os.path.dirname(__file__)
        self.MODELS_PATH = rf"{self.BASE_PATH}/models"