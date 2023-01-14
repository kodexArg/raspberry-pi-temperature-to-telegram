"""Capture a picture and save to disk

Returns:
    str: path of picture
"""

import cv2


def capture(picpath: str = "capture.jpg") -> str:
    capture = cv2.VideoCapture(0)
    _, image = capture.read()
    cv2.imwrite(picpath, image)
    return picpath
