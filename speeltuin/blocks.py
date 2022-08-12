import cv2
from pytesseract import pytesseract as pt
from PIL import Image

def calculate_ratio(width,height):
    '''
    Calculate aspect ratio for normal use case (w>h) and vertical text (h>w)
    '''
    ratio = width/height
    if ratio<1.0:
        ratio = 1./ratio
    return ratio

def compute_ratio_and_resize(img,width,height,model_height):
    '''
    Calculate ratio and resize correctly for both horizontal text
    and vertical case
    '''
    img2 = None
    ratio = width/height
    if ratio<1.0:
        ratio = calculate_ratio(width,height)
        img2 = cv2.resize(img,(model_height,int(model_height*ratio)), interpolation=Image.ANTIALIAS)
    else:
        img2 = cv2.resize(img,(int(model_height*ratio),model_height),interpolation=Image.ANTIALIAS)
    return img2,ratio

result = [
([112,3214,485,3317]),
([118,1748,474,2080]),
([118,1223,470,1479]),
([94,1179,508,2905]),
([119,73,577,99]),
([0,0,2481,63]),
([559,3197,1059,3286]),
([558,3095,1326,3139]),
([551,2761,915,2902]),
([997,2766,1396,2902]),
([551,2536,1364,2752]),
([552,2498,925,2527]),
([997,2498,1378,2639]),
([552,2386,1348,2489]),
([997,2273,1381,2377]),
([552,2236,951,2377]),
([524,2120,1066,2196]),
([998,2236,1402,2264]),
([1437,2352,1849,2902]),
([552,2046,1696,2081]),
([627,1941,707,1960]),
([627,1747,911,1780]),
([627,1533,976,1668]),
([552,1447,974,1480]),
([629,1372,1229,1405]),
([667,1222,1194,1330]),
([641,1071,643,1381]),
([2149,3103,2396,3189]),
([1902,2836,2370,2865]),
([1902,2724,2118,2751]),
([1891,2719,2397,2721]),
([1891,2646,2397,2648]),
([1891,2608,2397,2610]),
([1891,2534,2397,2536]),
([1902,2461,2134,2489]),
([1891,2456,2397,2458]),
([1891,2383,2397,2385]),
([1902,2316,2071,2338]),
([1891,2306,2397,2308]),
([1890,2233,1895,2721]),
([2393,2232,2398,2721]),
([1891,2233,2397,2235]),
([1442,2006,2396,2010]),
([1442,1858,2396,1862]),
([1442,1818,2397,1822]),
([1442,1745,2397,1749]),
([1442,1705,2397,1709]),
([1442,1633,1444,2008]),
([2394,1633,2396,2008]),
([1442,1632,2397,1636]),
([1441,1292,2396,1296]),
([1441,1070,1443,1295]),
([2394,1070,2396,1295]),
([1441,1069,2396,1073]),
([552,996,2135,1031]),
([629,928,1120,955]),
([629,847,1310,880]),
([1450,923,1704,958]),
([1450,848,1704,883]),
([629,772,1704,808]),
([629,697,1156,730]),
([629,622,1049,656]),
([1450,698,1704,733]),
([1450,623,1704,658]),
([629,547,1703,583]),
([628,472,1055,504]),
([629,397,1003,430]),
([545,79,897,86]),
([627,74,708,95]),
([1449,473,1705,508]),
([1450,398,1703,433]),
([2285,78,2395,95])]



img = cv2.imread("/home/rmast/175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.png", cv2.IMREAD_GRAYSCALE)
for x in result:
  xc = x[0]
  yc = 3509 - x[3]
  width = x[2] - xc
  height = x[3] - x[1] 
 # print(str(xc)+' '+str(yc)+' '+str(xd)+' '+str(yd)+' text')

  crop_img = None
  resized_img = None

  crop_img = img[yc : 3509 - x[1], xc:x[2]]
  #resized_img,ratio = compute_ratio_and_resize(crop_img,width,height,64)

  #ret = pt.image_to_boxes(crop_img, lang="nld", config="--psm 11 --dpi 300")
  ret = pt.image_to_data(crop_img, lang="nld", config="--psm 11 --dpi 300")
  print(ret)

