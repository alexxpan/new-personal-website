import matplotlib.pyplot as plt
import numpy as np
import skimage as sk
import skimage.io as skio
import skimage.filters as skfilters
import skimage.color as skcolor
import scipy.sparse as sparse
import skimage.transform as sktransform

im_target = sk.img_as_float(skio.imread('./imgs/boat-prague/prague.jpg'))
#im_target = sktransform.rescale(im_target, 0.5)
im_source = sk.img_as_float(skio.imread('./imgs/boat-prague/boat_aligned.png'))
im_mask = skcolor.rgb2gray(sk.img_as_float(skio.imread('./imgs/boat-prague/boat_mask.png')))

def blend_channel(im_target, im_source, im_mask):
    imh, imw = im_target.shape
    im2var = (np.arange(imh * imw)).reshape((imw, imh)).T
    b = np.zeros((imh*imw, 1))
    A = sparse.lil_matrix((imh*imw, imh*imw))

    e = 0
    for x in range(imh):
        for y in range(imw):
            #if im_mask[x,y] != 0:
                #print(im_mask[x,y])
            if im_mask[x,y] == 0:
                A[e, im2var[x,y]] = 1
                b[e] = im_target[x,y]
            elif im_mask[x,y] > 0:
                A[e, im2var[x,y]] = 4
                b[e] = (4*im_source[x,y]) - im_source[x+1,y] - im_source[x-1,y] - im_source[x,y+1] - im_source[x,y-1]

                if im_mask[x-1,y] == 0:
                    b[e] += im_target[x-1,y]
                else:
                    A[e, im2var[x-1,y]] = -1
                if im_mask[x+1,y] == 0:
                    b[e] += im_target[x+1,y]
                else:
                    A[e, im2var[x+1,y]] = -1
                if im_mask[x,y-1] == 0:
                    b[e] += im_target[x,y-1]
                else:
                    A[e, im2var[x,y-1]] = -1
                if im_mask[x,y+1] == 0:
                    b[e] += im_target[x,y+1]
                else:
                    A[e, im2var[x,y+1]] = -1
            e += 1

    A = sparse.csr_matrix(A)
    v = sparse.linalg.spsolve(A, b)
    v = v.reshape(imw,imh).T
    return v

def poisson_blend(im_target, im_source, im_mask):
    r = blend_channel(im_target[:,:,0], im_source[:,:,0], im_mask)
    g = blend_channel(im_target[:,:,1], im_source[:,:,1], im_mask)
    b = blend_channel(im_target[:,:,2], im_source[:,:,2], im_mask)
    im_out = np.dstack([r, g, b])
    return im_out


out = poisson_blend(im_target, im_source, im_mask)
out = np.clip(out,0,1)
skio.imsave("blended.jpg", out)
plt.imshow(out)
plt.show()


def naive_blend_channel(im_target, im_source, im_mask):
    imh, imw = im_target.shape
    v = im_target
    for x in range(imh):
        for y in range(imw):
            if im_mask[x,y] > 0:
                v[x,y] = im_source[x,y]
    return v
                
def naive_blend(im_target, im_source, im_mask):
    r = naive_blend_channel(im_target[:,:,0], im_source[:,:,0], im_mask)
    g = naive_blend_channel(im_target[:,:,1], im_source[:,:,1], im_mask)
    b = naive_blend_channel(im_target[:,:,2], im_source[:,:,2], im_mask)
    im_out = np.dstack([r, g, b])
    return im_out

#out = naive_blend(im_target, im_source, im_mask)
#out = np.clip(out,0,1)
#skio.imsave("naive.jpg", out) 
#plt.imshow(out)
#plt.show()

