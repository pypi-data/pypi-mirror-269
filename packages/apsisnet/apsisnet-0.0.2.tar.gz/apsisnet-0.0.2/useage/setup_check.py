from apsisnet import ApsisNet
from apsisnet.utils import LOG_INFO
import cv2

try:
    bnocr=ApsisNet()
    result=bnocr.infer([cv2.imread("./test.png")])
    LOG_INFO("--------------------------------------------------------------------------------------------",mcolor="red")
    LOG_INFO(result,mcolor="green")
    LOG_INFO("--------------------------------------------------------------------------------------------",mcolor="red")
    
except Exception as e:
    LOG_INFO("setup failed",mcolor="red")
    LOG_INFO("--------------------------------------------------------------------------------------------",mcolor="red")
    LOG_INFO(e,mcolor="green")
    LOG_INFO("--------------------------------------------------------------------------------------------",mcolor="red")
    