import numpy as np
from skimage.io import imread, imsave

def energy_map(image):
    im = np.gradient(image, axis = 0)
    energy = np.sqrt(im[:,:,0] ** 2 + im[:,:,1] ** 2 + im[:,:,2] ** 2) 
    return energy

def cumulative(energy):
    energy_map = np.zeros((energy.shape))
    for i in range(energy.shape[0]):
        for j in range(energy.shape[1]):
            if i == 0:
                energy_map[i][j] = energy[i][j]
            else:
                if j == 0:
                    energy_map[i][j] = energy[i][j] + min(energy[i - 1][j],energy[i - 1][j + 1])
                elif j == energy.shape[1] - 1:
                    energy_map[i][j] = energy[i][j] + min(energy[i - 1][j - 1],energy[i - 1][j])
                else:
                    energy_map[i][j] = energy[i][j] + min(energy[i - 1][j - 1],energy[i - 1][j], energy[i - 1][j + 1])
    return energy_map

def remove_seams(im, seam, energy):
    
    output = np.zeros((im.shape[0], im.shape[1] - 1, 3))
    output_energy = np.zeros((energy.shape[0], energy.shape[1] - 1))
    for i in range(im.shape[0]):        
        j = seam[i]
        output[i,:,0] = np.delete(im[i,:, 0],j)
        output[i,:,1] = np.delete(im[i,:, 1],j)
        output[i,:,2] = np.delete(im[i,:, 2],j)

        output_energy[i,:] = np.delete(energy[i,:],j)
    return output, output_energy

def carve(im, columns):
    energy = energy_map(im)
    cumulative_map = cumulative(energy)
    seams = []
    while columns > 0:
        seam = []
        for i in range(im.shape[0] - 1, -1, -1):
            if i == im.shape[0] - 1:
                last_line = cumulative_map[-1]
                m = np.argmin(last_line)
            else:

                if prev_m == 0:
                    m = np.argmin((cumulative_map[i, prev_m], cumulative_map[i, prev_m + 1]))
                    m = prev_m + m

                elif prev_m == im.shape[1] - 1:
                    m = np.argmin((cumulative_map[i, prev_m - 1], cumulative_map[i, prev_m]))
                    m = prev_m - 1 + m
                else:
                    m = np.argmin((cumulative_map[i, prev_m - 1], cumulative_map[i, prev_m], cumulative_map[i, prev_m + 1]))
                    m = prev_m - 1 + m
            prev_m = m
            seam.insert(0, m)
        seams.append(seam)
        columns -= 1
        im, energy = remove_seams(im, seam, energy)
        cumulative_map = cumulative(energy)
    return im, seams
horizontal_carve = True
vertical_carve = True
cuts = 150
image_name = "iceland"
image = imread('./' + image_name + '.jpg')

if horizontal_carve:
    carved, seams = carve(image, cuts)
    imsave('./horizontal_' + str(cuts) + image_name + '.jpg', carved/255.)
if vertical_carve:
    vertical = np.transpose(image, axes = (1,0,2))
    carved, seams = carve(vertical, cuts)
    imsave('./vertical_' + str(cuts) + image_name + '.jpg', np.transpose(carved, axes = (1,0,2)) / 255.)

def precompute(image, cuts, horizontal):
    if horizontal:
        carved, seams = carve(image, cuts)
    else:
        vertical = np.transpose(image, axes = (1,0,2))
        carved, seams = carve(vertical, cuts)
    f = open('seams.txt', 'w')
    f.write(str(seams))
    f.close()

def online(im, seams, amount):
    output = np.zeros((im.shape[0], im.shape[1] - 1, 3))
    if amount > len(seams):
        print("Not enough seams precomputed")
        amount = len(seams)
    for k in range(amount):
        seam = seams[k]
        for i in range(im.shape[0]):
            j = seam[i]
            output[i,:,0] = np.delete(im[i,:, 0],j)
            output[i,:,1] = np.delete(im[i,:, 1],j)
            output[i,:,2] = np.delete(im[i,:, 2],j)
    return output

#precompute(image, 200, True)
onl = False
if onl:
    f = open('seams.txt', 'r')
    seams = [[int(s) for s in st.split(',')] for st in f.read()[2:-2].split('], [')]
    imsave('./testonline.jpg', online(image, seams, 129)/255.)

