import cv2
import easyocr
import numpy as np
from PIL import Image
from collections import Counter

def complementing_colors(image):
    colors = Counter(image.reshape(-1, image.shape[-1]))
    return colors.most_common(2)

def invert_text_color(image, light_color, dark_color):
    mask = np.all(image == light_color, axis=-1)
    image[mask] = dark_color
    image[~mask] = light_color
    return image

def main():
    # Read the A4 image
    input_file = '175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg'
    img = cv2.imread(input_file)

    # Initialize EasyOCR
    reader = easyocr.Reader(['nl'])

    # Detect tetragons containing a line of text
    result = reader.readtext(img, detail=0, text_threshold=0.5, link_threshold=0.2)

    # Create a bitonal mask with the original resolution
    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    # Process each tetragon
    for i, text in enumerate(result):
        # Extract the region of interest (ROI)
        x, y, w, h = [int(coord) for coord in text.split(',')[:4]]
        roi = img[y:y+h, x:x+w]

        # Find the two most complementing colors
        color1, color2 = complementing_colors(roi)

        # Invert text color if needed
        roi = invert_text_color(roi, color1[0], color2[0])

        # Binarize the ROI
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, roi_bin = cv2.threshold(roi_gray, 128, 255, cv2.THRESH_BINARY)

        # Add the binarized ROI to the bitonal mask
        mask[y:y+h, x:x+w] = roi_bin

    # Save the bitonal mask
    output_file = 'a4_bitonal_mask.png'
    cv2.imwrite(output_file, mask)

if __name__ == '__main__':
    main()
