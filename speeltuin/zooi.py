import tgon
import easyocr
reader = easyocr.Reader(['nl','en']) # this needs to run only once to load the model into memory
result = reader.detect('/home/rmast/175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg')

x0, y0, x1, y1, x2, y2, x3, y3 = 107, 181, 500, 181, 500, 306, 107, 306
rect_obj = tgon.PyRectangle(x0, y0, x1, y1, x2, y2, x3, y3)
print(dir(rect_obj))

from PIL import Image
image = Image.open("/home/rmast/175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg")

print(rect_obj.otsu_threshold_tetragon(image,result))
