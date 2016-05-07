import cv2 as cv
import sys
import numpy as np
sys.path.append('../scripts')
from OptimalThresholding import optimal_thresholding

# load gray images
imageColor = cv.imread('../images/assignment4/LungCancerTumor.jpg')
imageGray = cv.imread('../images/assignment4/LungCancerTumor.jpg', cv.IMREAD_GRAYSCALE)

# ---------------------------Global thresholding--------------------------------------- #

thresholded_image , optimal_threshold = optimal_thresholding(imageGray)
print "global threshold using optimal thresholding method = ", optimal_threshold

# ---------------------------local thresholding---------------------------------------- #

# convert image to square image
resized_image = cv.resize(imageGray, (imageGray.shape[0], imageGray.shape[0]))
blocks_image = np.zeros(resized_image.shape)

# block size should be > 4!
block_size = 10

if block_size <= 4:
    print "Error in local thresholding , block size should be greater than 4 ! "
    exit()

if block_size > resized_image.shape[0]:
    print "Error local thresholding , block size should be smaller than image size!"
    exit()

for r in range(0, resized_image.shape[0],block_size):
    for c in range(0, resized_image.shape[1],block_size):
        block = resized_image[r:min(r + block_size, resized_image.shape[0]) , c:min(c + block_size, resized_image.shape[1])]
        thresholded_block, threshold = optimal_thresholding(block)
        blocks_image[r:min(r + block_size, resized_image.shape[0]) ,
                     c:min(c + block_size, resized_image.shape[1])] = thresholded_block

# convert image back to original size
blocks_image = cv.resize(blocks_image, (imageGray.shape[1], imageGray.shape[0]))

# display all images
cv.imshow('Original image', imageGray)
cv.imshow('global thresholding', thresholded_image)
window_name = "local thresholding of block size " + str(block_size)
cv.imshow(window_name, blocks_image)
cv.waitKey(0)
cv.destroyAllWindows()

