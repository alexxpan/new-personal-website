import matplotlib.pyplot as plt
from align_image_code import align_images
import numpy as np
import skimage as sk
import skimage.io as skio
import skimage.filters as skfilters
import skimage.color as skcolor

# First load images

# high sf
im1 = plt.imread('./imgs/dog.jpg')/255.

# low sf
im2 = plt.imread('./imgs/bear.jpg')/255.

# Next align images (this code is provided, but may be improved)
im1_aligned, im2_aligned = align_images(im1, im2)

# Code for creating hybrid images

def low_pass(im, sigma, color):
    if not color:
        im = skcolor.rgb2gray(im)
        low_pass_im = skfilters.gaussian(im, sigma=sigma, multichannel=False)
    else:
        low_pass_im = skfilters.gaussian(im, sigma=sigma, multichannel=True)
    return low_pass_im

def high_pass(im, sigma, color):
    low_pass_im = low_pass(im, sigma, color)
    if not color:
        im = skcolor.rgb2gray(im)
    high_pass_im = im - low_pass_im
    if color:
        high_pass_im = np.clip(high_pass_im, 0, 1)
    return high_pass_im

def hybrid_image(im1, im2, sigma1, sigma2, color=False):
    # im1 will be low frequency, im2 will be high frequency
    return low_pass(im1, sigma1, color) + high_pass(im2, sigma2, color)

#hybrid = hybrid_image(im1_aligned, im2_aligned, 6, 5)
#plt.imshow(hybrid, cmap="gray")
#plt.show()

def hybrid_image_color(im1, im2, sigma1, sigma2, im1_color, im2_color):
    if im1_color and im2_color:
        return np.clip(hybrid_image(im1, im2, sigma1, sigma2, True), 0, 1)
    if not im1_color and not im2_color:
        return hybrid_image(im1, im2, sigma1, sigma2, False)
    if im1_color and not im2_color:
        low = low_pass(im1, sigma1, color=True)
        high_channel = np.clip(high_pass(im2, sigma2, color=False), 0, 1)
        high = np.dstack([high_channel, high_channel, high_channel])
        return np.clip(low + high, 0, 1)
    if not im1_color and im2_color:
        low_channel = low_pass(im1, sigma1, color=False)
        low = np.dstack([low_channel, low_channel, low_channel])
        high = high_pass(im2, sigma2, color=True)
        return np.clip(low + high, 0, 1)

#hybrid = hybrid_image_color(im1_aligned, im2_aligned, 6, 5, False, True)
#plt.imshow(hybrid)
#plt.show()

# Fourier analysis (for dog-bear)
def fourier(im):
    return np.log(np.abs(np.fft.fftshift(np.fft.fft2(im))))

#plt.imshow(fourier(skcolor.rgb2gray(im1_aligned)), cmap="gray")
#plt.imshow(fourier(skcolor.rgb2gray(im2_aligned)), cmap="gray")
#plt.imshow(fourier(low_pass(im1_aligned, 6)), cmap="gray")
#plt.imshow(fourier(high_pass(im2_aligned, 5)), cmap="gray")
#plt.imshow(fourier(hybrid), cmap="gray")
#plt.show()

'''
## Compute and display Gaussian and Laplacian Stacks
## You also need to supply this function
N = 5 # suggested number of stack levels (your choice)
stacks(hybrid, N)
'''

def stacks(hybrid, N):
    gaussian_stack = hybrid
    curr_gaussian = hybrid
    sigma = 2
    for i in range(1, N):
        low_pass_im = skfilters.gaussian(curr_gaussian, sigma=sigma, multichannel=False)
        gaussian_stack = np.dstack((gaussian_stack, low_pass_im))
        curr_gaussian = low_pass_im
        sigma *= 2
    laplacian_stack = hybrid - gaussian_stack[:,:,0]
    for i in range(1, N):
        laplacian_stack = np.dstack((laplacian_stack, gaussian_stack[:,:,i-1] - gaussian_stack[:,:,i]))
    return gaussian_stack, laplacian_stack

hybrid = skcolor.rgb2gray(plt.imread('./imgs/lincoln.jpg')/255.)
gaussian_stack, laplacian_stack = stacks(hybrid, 5)
show = laplacian_stack[:,:,4]
plt.imshow(show, cmap="gray")
plt.show()

