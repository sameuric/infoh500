
# Imports
import numpy as np
from matplotlib import pyplot as plt
from skimage.io import imread, imsave
from numpy.fft import fft2, ifft2, fftshift, ifftshift



# Automatic dithering and noise reduction using a low-pass filter
#
# The idea is to reduce the dithering in a given image by
# building a low-pass filter. The main point here is to
# detect the best radius for the disk shaped mask.

def fourier(im):
    return fftshift(fft2(im))

def ifourier(f):
    return ifft2(ifftshift(f)).real

# Quick function to create a disk shaped mask to apply to our Fourier image
def get_disk_mask(r, imshape):
    a, b = imshape[0]//2, imshape[1]//2
    y,x = np.ogrid[-a:imshape[0]-a, -b:imshape[1]-b]
    mask = x*x + y*y <= r*r
    return mask

# Compute the sum of all complex number's amplitude
# of a given matrix filled with complex numbers
def compute_energy(matrix):
    amplitude = np.abs(matrix)
    return amplitude.sum()



# Open one image and use the Fourier transform on it
img = imread('img/noisy.jpg')
f = fourier(img)


# Energy of the initial image
max_energy = compute_energy(f)
if max_energy <= 0:
    raise Exception('Empty image?')


# Detect the best radius (attempt with a ratio energy / max_energy = 12%)
radius = 0
energy = 0

while energy / max_energy < 0.12:
    radius = radius + 1
    mask = get_disk_mask(radius, f.shape)
    energy = compute_energy(f*mask)


# Get the image back to spatial domain
f2 = f*mask
final_img = ifourier(f2)
plt.imsave('final_p2.png', final_img, cmap=plt.cm.gray, vmin=0, vmax=255)



# Show result
print("Final computed radius:", radius)

plt.figure(figsize=(15,8))
plt.subplot(1,2,1)
plt.imshow(final_img, cmap=plt.cm.gray, vmin=0, vmax=255, interpolation='none')
plt.title('Image filtered')
plt.axis('off')
plt.subplot(1,2,2)
plt.imshow(np.log(np.abs(f2), where=np.abs(f2)>0), interpolation='none', cmap='viridis')
plt.title('Log of Fourier amplitude')
plt.axis('off')
plt.show()







