import matplotlib.pyplot as plt
import numpy as np
import skimage as sk
import skimage.io as skio
import skimage.filters as skfilters
import skimage.color as skcolor
import scipy.sparse as sparse

im = plt.imread('./toy_in.jpg')/255.

imh, imw = im.shape
im2var = (np.arange(imh * imw)).reshape((imw, imh)).T

b = np.zeros((2*imh*imw+1, 1))
A = sparse.lil_matrix((2*imh*imw+1, imh*imw))

e = 0

for x in range(imh):
    for y in range(imw-1):
        A[e, im2var[x,y+1]] = 1
        A[e, im2var[x,y]] = -1
        b[e] = im[x,y+1] - im[x,y]
        e += 1

for x in range(imh-1):
    for y in range(imw):
        A[e, im2var[x+1,y]] = 1
        A[e, im2var[x,y]] = -1
        b[e] = im[x+1,y] - im[x,y]
        e += 1

e += 1
A[e, im2var[0,0]] = 1
b[e] = im[0,0]

A = sparse.csr_matrix(A)
v = sparse.linalg.lsqr(A, b)[0]
v = v.reshape(imw,imh).T

error = np.sum(np.absolute(im - v))
print(error)

skio.imsave("toy_out.jpg", v)
plt.imshow(v, cmap="gray")
plt.show()
