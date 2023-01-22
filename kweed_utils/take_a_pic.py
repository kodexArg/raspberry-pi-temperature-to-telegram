"""Capture a picture and save to disk

Returns:
    str: path of picture
"""

import cv2


def capture(pic_path: str = "capture.jpg") -> str:
    capture = cv2.VideoCapture(0)
    _, image = capture.read()
    cv2.imwrite(pic_path, image)
    return pic_path
