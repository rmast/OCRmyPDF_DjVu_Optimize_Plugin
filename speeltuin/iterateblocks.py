from PIL import Image
import tesserocr

import numpy as np
import cv2
import matplotlib.pyplot as plt
import pytesseract

image = Image.open("/home/rmast/175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.png")

with tesserocr.PyTessBaseAPI(path='/usr/local/share/tessdata5', lang='lat+eng+Latin+nld', oem=0, psm=tesserocr.PSM.OSD_ONLY) as api:
    api.SetImage(image)
    api.SetVariable('clean_noise',"0")
    api.SetVariable('textord_noise_debug',"1")
    boxes = api.GetComponentImages(tesserocr.RIL.BLOCK, True)
    delta = 5 

    image_array = np.array(image)
    for box in boxes:
        print(box)
        box = box[1]
        x, y, w, h = box['x'] - delta, box['y'] - delta, box['w'] + 2 * delta, box['h'] + 2 * delta
        cv2.line(image_array, (x, y), (x + w, y), (0, 0, 0), 2)
        cv2.line(image_array, (x, y), (x, y + h), (0, 0, 0), 2)
        cv2.line(image_array, (x + w, y), (x + w, y + h), (0, 0, 0), 2)
        cv2.line(image_array, (x, y + h), (x + w, y + h), (0, 0, 0), 2)
    plt.imshow(image_array)
    plt.show()

    #for i, (im, box, _, _) in enumerate(boxes):
         #print(i,  (im, box, _, _))
         #api.SetRectangle(box['x'] - delta, box['y'] - delta, box['w'] + 2 * delta, box['h'] + 2 * delta) 
#
    #api.Recognize()
    #ri = api.GetIterator()
    #font = []
    #attributes = []
    #for r in iterate_level(ri, RIL.BLOCK):
        #symbol = r.GetUTF8Text(RIL.BLOCK)
        #conf = r.Confidence(RIL.BLOCK)
        #symbol = symbol.replace('\n',' ').replace(' ', '')
        #word_attributes = r.WordFontAttributes()
        #if not symbol:
            #continue
        #else:
            #font.append([symbol, 'confidence: ',conf])
            #attributes.append(word_attributes)
        #
        #return font, attributes
