# main.py
import sys
import tgon
import easyocr
from PIL import Image

if __name__ == "__main__":
    #print(f"Arguments count: {len(sys.argv)}")
    #for i, arg in enumerate(sys.argv):
        #print(f"Argument {i:>6}: {arg}")
    if len(sys.argv) > 1:
        imagename = sys.argv[1]
        reader = easyocr.Reader(['nl','en']) # this needs to run only once to load the model into memory
        result = reader.detect(imagename)
        print(result)
        image = Image.open(imagename)
        rect_obj=tgon.PyRectangle(image)
        rect_obj.otsu_threshold_tetragon(result)
