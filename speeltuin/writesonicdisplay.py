import cv2
import numpy as np
import easyocr

# Load image
img = cv2.imread('175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg')

# Initialize EasyOCR reader
reader = easyocr.Reader(['nl'])

# Detect text boxes in the image
boxes = reader.detect(img)

# Loop over every detected box
for box in boxes:
    # Extract tetragon coordinates
    poly = np.array(box[0]).reshape((-1, 1, 2)).astype(np.int32)
    print (poly)
    
    ## Create mask of tetragon
    #mask = np.zeros(img.shape[:2], dtype=np.uint8)
    #cv2.fillPoly(mask, [poly], (255, 255, 255))
    
    # Crop image to tetragon
    #crop = cv2.bitwise_and(img, img, mask=mask)
    x, y, w, h = cv2.boundingRect(poly)
    print (x, y, w, h)
    #crop = crop[y:y+h, x:x+w]
    
    # Invert colors of text in tetragon
    #crop = cv2.bitwise_not(crop)
    
    # Display cropped tetragon
    #cv2.imshow("Tetragon", crop)
    #cv2.waitKey(0)
    
# Close all windows
#cv2.destroyAllWindows()
