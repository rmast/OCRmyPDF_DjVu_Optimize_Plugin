import cv2
import numpy as np
import easyocr

# Load the input image
img = cv2.imread('175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg')
imgo = img

# Initialize the EasyOCR reader
reader = easyocr.Reader(['nl'])

# Detect the text boxes in the image
boxes = reader.detect(img)

# Loop through the detected text boxes
for box in boxes:
    # Extract the tetragon from the input image
    pts = np.array(box[0]).reshape((-1, 1, 2)).astype(np.int32)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, np.array([pts], dtype=np.int32), 255)

    # apply the mask to the image
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    # crop the masked image to the tetragon size
    x, y, w, h = cv2.boundingRect(np.array([box]))
    cropped_img = masked_img[y:y+h, x:x+w]

    # display the cropped image
    cv2.imshow('Tetragon', cropped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#    tetragon = cv2.polylines(img, [pts], True, (0, 255, 255), thickness=2, lineType=cv2.LINE_AA)
#    tetragon_mask = np.zeros(img.shape[:2], dtype=np.uint8)
#    cv2.drawContours(tetragon_mask, [pts], 0, 255, -1)

    # Calculate the Otsu threshold of the tetragon
#    gray_tetragon = cv2.cvtColor(tetragon, cv2.COLOR_BGR2GRAY)
#    otsu_threshold, _ = cv2.threshold(gray_tetragon, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
#    cv2.imshow('Result', tetragon)
#    cv2.waitKey(0)
#    cv2.imshow('Result', tetragon_mask)
#    cv2.waitKey(0)
#    exit
#    # Invert the content of the tetragon if the surrounding color is light
#    mean_val = cv2.mean(tetragon, tetragon_mask)[0]
#    if mean_val > 128:
#        tetragon = cv2.bitwise_not(tetragon)
#
#    # Create a mask of the tetragon and apply it to the input image
#    tetragon_mask = cv2.bitwise_not(tetragon_mask)
#    imgo = cv2.bitwise_and(img, img, mask=tetragon_mask)
#    imgo = cv2.bitwise_or(img, tetragon)
#
# Save the resulting image as result_image.png
#cv2.imwrite('result_image.png', imgo)
