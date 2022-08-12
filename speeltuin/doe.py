#import torch
#import torchvision
from torchvision.io import read_image, write_png
#from torch.nn.functional import interpolate
#img = read_image("/home/rmast/175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg")
#groter = interpolate(img, scale_factor=4, mode='linear')
#write_png(groter,"/home/rmast/erggroot.png")
from PIL import Image

import cv2
import numpy as np
import torch
import torch.nn.functional as F

IMAGE_PATH = "/home/rmast/175789293-f39ddfdb-6f3e-4598-8d16-80a1f4a88b36.jpg"
 # open image and mask files
image = cv2.imread(IMAGE_PATH, cv2.IMREAD_COLOR)

# convert to torch tensor
image2 = torch.from_numpy(image).permute(2, 0, 1).float()  # HWC to CHW and byte to float

# upsample image and mask by 4x
image3 = F.interpolate(image2.unsqueeze(0), scale_factor=4, mode='bilinear', align_corners=False)
#cv2.imwrite("/home/rmast/tegroot.png", image)

write_png(image3,"/home/rmast/erggroot.png")

