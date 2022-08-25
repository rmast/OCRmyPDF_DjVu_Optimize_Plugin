import tesserocr
import csv
import numpy as np
import cv2
import pytesseract
from PIL import Image
import matplotlib as mpl

import matplotlib.pyplot as plt
#img3 = cv2.imread('/home/rmast/plaatjes/out107-181-393-125.png')
img3 = cv2.imread('/home/rmast/plaatjes/out1496-3078-212-39.png')
h, w, _ = img3.shape # assumes color image
pytess_result = pytesseract.image_to_boxes(img3, lang='nld+lat+Latin+eng',
        config="--psm 7 -c tessedit_create_boxfile=1", output_type=pytesseract.Output.DICT)
        #config="--psm 7 --oem 0 -c tessedit_create_boxfile=1", output_type=pytesseract.Output.DICT)
print(pytess_result)
for j in range(0, len(pytess_result["char"])):
    left = pytess_result["left"][j]
    bottom = pytess_result["bottom"][j]
    right = pytess_result["right"][j]
    top = pytess_result["top"][j]
    cv2.rectangle(img3, (left, h - top - 1), (right, h - bottom - 1), (255, 0, 0), 1)
mpl.use('tkAgg')
plt.imshow(img3)
plt.show()
