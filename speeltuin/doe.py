#import torch
import matplotlib.pyplot as plt
import matplotlib as mpl
#import torchvision
from torchvision.io import read_image, write_png
from torchvision.transforms.functional import convert_image_dtype
#from torch.nn.functional import interpolate
#img = read_image("/home/rmast/175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg")
#groter = interpolate(img, scale_factor=4, mode='linear')
#write_png(groter,"/home/rmast/erggroot.png")
from PIL import Image

#import cv2
import numpy as np
import torch
import torch.nn.functional as F

IMAGE_PATH = "/home/rmast/175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg"
img = Image.open(IMAGE_PATH)
img_arr = np.array(img)[:, :, :3] # remove alpha channel
 # open image and mask files
#image = cv2.imread(IMAGE_PATH, cv2.IMREAD_COLOR)

mpl.use('tkAgg')
plt.imshow(img_arr)
plt.show()
# convert to torch tensor
image2 = torch.from_numpy(img_arr).permute(2, 0, 1).unsqueeze(0).float()  # HWC to CHW and byte to float

# upsample image and mask by 4x
image3 = F.interpolate(image2, scale_factor=4, mode='bilinear', align_corners=False)
#cv2.imwrite("/home/rmast/tegroot.png", image)
array = image3[0].permute(1, 2, 0).byte().numpy()
#image4 = convert_image_dtype(image= image3, dtype= torch.uint8)
plt.imshow(array)
plt.show()
#write_png(image3[0].permute(1, 2, 0).byte().numpy(),"/home/rmast/erggroot.png")

im = Image.fromarray(array)
im.save("/home/rmast/erggroot.png")
