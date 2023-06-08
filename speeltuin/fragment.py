import easyocr
import cv2
import numpy as np

#Divide the input image into overlapping patches. Ensure that the overlap is enough to prevent missing any text regions near the patch boundaries.
def get_image_patches(image, patch_size, overlap):
    height, width, _ = image.shape
    patches = []
    patch_info = []

    y_step = int(patch_size[0] * (1 - overlap))
    x_step = int(patch_size[1] * (1 - overlap))

    for y in range(0, height, y_step):
        for x in range(0, width, x_step):
            y_end = min(height, y + patch_size[0])
            x_end = min(width, x + patch_size[1])

            patch = image[y:y_end, x:x_end, :]
            patches.append(patch)
            patch_info.append((y, x))

    return patches, patch_info
#Modify the test_net function: Update the test_net function in craft.py to accept an additional parameter, patch_info. Modify the code that calculates the bounding boxes to take into account the patch's position within the original image.
#python
#Copy
def test_net(net, image, text_threshold, link_threshold, low_text, cuda, poly, patch_info=None):
    # ...
    # After getting bounding boxes (bboxes) and scores
    if patch_info:
        dy, dx = patch_info
        bboxes[:, [0, 2]] += dx
        bboxes[:, [1, 3]] += dy
    # ...
#Process each patch: Divide the input image into patches and process each patch with the modified test_net function.
img = cv2.imread('175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg')
image = load_image(...)
patch_size = (1280, 1280)  # Adapt this according to your VRAM constraints
overlap = 0.2  # Overlap ratio

# Get patches and patch_info
patches, patch_info_list = get_image_patches(image, patch_size, overlap)

results = []
for patch, patch_info in zip(patches, patch_info_list):
    result = test_net(net, patch, text_threshold, link_threshold, low_text, cuda, poly, patch_info)
    results.append(result)
img = cv2.imread('175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg')

# Define the patch size (e.g. quarter of the page)
patch_size = (img.shape[1]//2, img.shape[0]//2)

# Define the overlap size (e.g. 50% overlap)
overlap_size = (patch_size[0]//2, patch_size[1]//2)

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Loop over the patches
results = []
for x in range(0, img.shape[1], patch_size[0]-overlap_size[0]):
    for y in range(0, img.shape[0], patch_size[1]-overlap_size[1]):
        # Extract the patch
        patch = img[y:y+patch_size[1], x:x+patch_size[0], :]
       
        # Perform EasyOCR detection on the patch
        patch_results = reader.readtext(patch)
       
        # Shift the bounding boxes back to the original image coordinates
        for res in patch_results:
            res[0] += x
            res[1] += y
       
        # Add the patch results to the overall results list
        results.extend(patch_results)

# Group the results based on proximity
clusters = []
for res in results:
    added = False
    for cluster in clusters:
        if np.linalg.norm(np.array(res[0][:2]) - np.array(cluster[0][:2])) < 50:
            cluster.append(res)
            added = True
            break
    if not added:
        clusters.append([res])

# Compute the final results for each cluster (e.g. by taking the majority vote)
final_results = []
for cluster in clusters:
    # Choose the most common text
    texts = [res[1] for res in cluster]
    text_counts = {text:

#Deze tekst komt van Poe.com:
#https://github.com/JaidedAI/EasyOCR/blob/master/easyocr/craft.py contains a model that uses too much VRAM given an input shape of 1,3,2560,2560 and 2 GB VRAM.
#Splitting up the shape to about a quarter would fit in the VRAM. What can I change in this model to split up processing in such a way processing would use about only a third of VRAM? At what functions can I chop up the processing in a way I could put the partial answers together again at the end?
#
#To reduce the VRAM usage of the EasyOCR model, you can split the input image into smaller patches and process them separately. The EasyOCR model in craft.py uses the CRAFT text detection algorithm, and you can modify the code to handle smaller image patches without significantly impacting the overall performance.
#
#Here's a high-level approach to achieve this:
#
#
#Modify the test_net function in craft.py to accept an additional parameter, patch_info, which contains information about the current patch (e.g., its location within the original image).
#
#Process each patch through the modified test_net function and collect the results.
#
#Merge the results from all patches to get the final text regions for the original image.
#
#Here's a more detailed outline of the changes you need to implement:
#
#Divide the input image into patches: You can use a function like this to divide the input image into overlapping patches:
#python
#Copy
#Merge the results: Combine the results from all the patches to get the final text regions for the original image. You can merge the results by concatenating the lists of bounding boxes and scores from each patch.
#python
#Copy
merged_bboxes = np.concatenate([r[0] for r in results], axis=0)
merged_scores = np.concatenate([r[1] for r in results], axis=0)
#Keep in mind that this approach may introduce duplicate detections for text regions near the patch boundaries. You might need to implement a post-processing step to remove these duplicates or merge overlapping boxes.

#This should allow you to process large images with reduced VRAM requirements. Note that the processing time may increase due to the overhead of processing multiple patches and merging the results.
