import matplotlib.pyplot as plt
import numpy as np
import skimage as sk
import skimage.io as skio
import skimage.filters as skfilters
import skimage.color as skcolor

im1 = plt.imread('./apple.jpg')
im2 = plt.imread('./orange.jpg')
mask = plt.imread('./apple-mask.jpg')

def make_gaussian(im, N):
    im = skcolor.rgb2gray(im)
    gaussian_stack = im
    curr_gaussian = im
    sigma = 4
    for i in range(1, N):
        low_pass_im = skfilters.gaussian(curr_gaussian, sigma=sigma, multichannel=False)
        gaussian_stack = np.dstack((gaussian_stack, low_pass_im))
        curr_gaussian = low_pass_im
        sigma *= 2
    return gaussian_stack

def make_laplacian(im, N):
    gaussian_stack = make_gaussian(im, N)
    im = skcolor.rgb2gray(im)
    laplacian_stack = im - gaussian_stack[:,:,0]
    for i in range(1, N):
        laplacian_stack = np.dstack((laplacian_stack, gaussian_stack[:,:,i-1] - gaussian_stack[:,:,i]))
    return laplacian_stack

def blend(im1, im2, mask, N):
    if len(im1.shape) == 3 and len(im2.shape) == 3:
        l1 = make_laplacian(skcolor.rgb2gray(im1), N)
        l2 = make_laplacian(skcolor.rgb2gray(im2), N)
    else:
        l1 = make_laplacian(im1, N)
        l2 = make_laplacian(im2, N)

    gr = make_gaussian(mask, N)
    ls = (gr * l1) + ((1 - gr) * l2)
    blended = ls[:,:,0]
    for i in range(1, N):
        blended = blended + ls[:,:,i]
    return blended
    
out = blend(im1, im2, mask, 5)
plt.imshow(out, cmap="gray")
plt.show()

def blend_color(im1, im2, mask, N):
   r = blend(im1[:,:,0], im2[:,:,0], mask, N)
   g = blend(im1[:,:,1], im2[:,:,1], mask, N)
   b = blend(im1[:,:,2], im2[:,:,2], mask, N)
   return np.dstack([r,g,b])

#out_color = blend_color(im1, im2, mask, 5)
#out_color = out_color - np.min(out_color)
#out_color = out_color / np.max(out_color)
#plt.imshow(out_color)
#plt.show()





