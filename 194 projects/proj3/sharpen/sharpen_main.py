import numpy as np
import skimage as sk
import skimage.io as skio
import skimage.filters as skfilters

im = skio.imread("example.jpg")
im = sk.img_as_float(im)

low_pass = skfilters.gaussian(im, sigma=5, multichannel=True)
high_pass = im - low_pass 
a = 10
sharpened = np.clip(im + (a * high_pass), 0, 1)

skio.imshow(sharpened)
skio.show()
#skio.imsave("mask.jpg", sharpened)
