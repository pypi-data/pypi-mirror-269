#-*- coding: utf-8 -*-
from __future__ import print_function
import warnings
warnings.filterwarnings('ignore')
#-------------------------
# imports
#-------------------------
from abc import ABCMeta, abstractmethod

class Recognizer(metaclass=ABCMeta):
    """Recognizer base class
    """
    def __init__(self):
        pass
    
    @abstractmethod
    def infer(self):
        pass
