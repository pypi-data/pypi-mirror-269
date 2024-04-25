import numpy as np
import cv2
import logging
import logging.config
from os import path

log_file_path = path.join(path.dirname(path.abspath(__name__)), 'logger.config')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("ColorRecognition")

__cube = {
    1: "",
    2: "",
    3: "",
    4: "",
    5: "",
    6: "",
    7: "",
    8: ""
}


def getColors(screenshotNumber, screenshot):
    frame = cv2.imread(screenshot)
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    lower_yellow = np.array([110, 185, 190])
    upper_yellow = np.array([130, 260, 235])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    lower_blue = np.array([60, 240, 160])
    upper_blue = np.array([117, 260, 202])
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    lower_red = np.array([135, 210, 160])
    upper_red = np.array([155, 225, 255])
    red_mask = cv2.inRange(hsv, lower_red, upper_red)

    cv2.rectangle(hsv, (575, 275), (625, 325), (255, 255, 255), 3)
    roi_bottom_left = hsv[270:310, 570:610]
    average_color_bottom_left = np.mean(roi_bottom_left, axis=(0, 1))

    cv2.rectangle(hsv, (650, 275), (700, 325), (255, 255, 255), 3)
    roi_bottom_right = hsv[270:310, 670:710]
    average_color_bottom_right = np.mean(roi_bottom_right, axis=(0, 1))

    cv2.rectangle(hsv, (575, 100), (625, 150), (255, 255, 255), 3)
    roi_above_left = hsv[85:120, 580:620]
    average_color_above_left = np.mean(roi_above_left, axis=(0, 1))

    cv2.rectangle(hsv, (650, 100), (700, 150), (255, 255, 255), 3)
    roi_above_right = hsv[85:120, 670:710]
    average_color_above_right = np.mean(roi_above_right, axis=(0, 1))

    logging.debug("average_color_bottom_left " + str(average_color_bottom_left))

    if (average_color_bottom_left >= lower_yellow).all() and (average_color_bottom_left <= upper_yellow).all():
        if (screenshotNumber == 1):
            __cube[1] = 'Yellow'
        if (screenshotNumber == 2):
            __cube[5] = 'Yellow'
    if (average_color_bottom_left >= lower_blue).all() and (average_color_bottom_left <= upper_blue).all():
        if (screenshotNumber == 1):
            __cube[1] = 'Blue'
        if (screenshotNumber == 2):
            __cube[5] = 'Blue'
    if (average_color_bottom_left >= lower_red).all() and (average_color_bottom_left <= upper_red).all():
        if (screenshotNumber == 1):
            __cube[1] = 'Red'
        if (screenshotNumber == 2):
            __cube[5] = 'Red'
    logging.debug("average_color_bottom_right " + str(average_color_bottom_right))

    if (average_color_bottom_right >= lower_yellow).all() and (average_color_bottom_right <= upper_yellow).all():
        if (screenshotNumber == 1):
            __cube[2] = 'Yellow'
        if (screenshotNumber == 2):
            __cube[6] = 'Yellow'
    if (average_color_bottom_right >= lower_blue).all() and (average_color_bottom_right <= upper_blue).all():
        if (screenshotNumber == 1):
            __cube[2] = 'Blue'
        if (screenshotNumber == 2):
            __cube[6] = 'Blue'
    if (average_color_bottom_right >= lower_red).all() and (average_color_bottom_right <= upper_red).all():
        if (screenshotNumber == 1):
            __cube[2] = 'Red'
        if (screenshotNumber == 2):
            __cube[6] = 'Red'
    logging.debug("average_color_above_left " + str(average_color_above_left))

    if (average_color_above_left >= lower_yellow).all() and (average_color_above_left <= upper_yellow).all():
        if (screenshotNumber == 1):
            __cube[7] = 'Yellow'
        if (screenshotNumber == 2):
            __cube[3] = 'Yellow'
    if (average_color_above_left >= lower_blue).all() and (average_color_above_left <= upper_blue).all():
        if (screenshotNumber == 1):
            __cube[7] = 'Blue'
        if (screenshotNumber == 2):
            __cube[3] = 'Blue'
    if (average_color_above_left >= lower_red).all() and (average_color_above_left <= upper_red).all():
        if (screenshotNumber == 1):
            __cube[7] = 'Red'
        if (screenshotNumber == 2):
            __cube[3] = 'Red'
    logging.debug("average_color_above_right " + str(average_color_above_right))

    if (average_color_above_right >= lower_yellow).all() and (average_color_above_right <= upper_yellow).all():
        if (screenshotNumber == 1):
            __cube[8] = 'Yellow'
        if (screenshotNumber == 2):
            __cube[4] = 'Yellow'
    if (average_color_above_right >= lower_blue).all() and (average_color_above_right <= upper_blue).all():
        if (screenshotNumber == 1):
            __cube[8] = 'Blue'
        if (screenshotNumber == 2):
            __cube[4] = 'Blue'
    if (average_color_above_right >= lower_red).all() and (average_color_above_right <= upper_red).all():
        if (screenshotNumber == 1):
            __cube[8] = 'Red'
        if (screenshotNumber == 2):
            __cube[4] = 'Red'

def getResult():
    logging.info("getResult: " + str(__cube))
    return __cube