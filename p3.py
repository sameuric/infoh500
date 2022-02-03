# Sacha MEURICE
# Project INFO-H500
# Part 3


# Imports
from skimage.feature import peak_local_max
from skimage.io import imread
from skimage import img_as_ubyte
import skimage.filters.rank as skr
from skimage.morphology import disk
from skimage.measure import label


# Read the image in grayscale and
# set unsigned bytes values to each pixel
brain_img = img_as_ubyte(imread("mri_brain.jpg", as_gray=True))

# Store height and width
im_h, im_w = brain_img.shape[0:2]


# Compute gradient
gradient = skr.gradient(skr.median(brain_img, disk(5)), disk(3))
gradient_i = gradient.max()-gradient # inverse gradient image so that local minima -> local maxima
markers_coords = peak_local_max(gradient_i, threshold_rel=0.99, min_distance=10)


# create markers:
markers = np.zeros_like(gradient).astype('bool')
markers[tuple(markers_coords.T)] = True

# label and watershed
markers = label(markers)
ws = watershed(gradient, markers)

# Compute a score for each region
# depending on blank level and region's size
def compute_score(region, w, h):
    score = 0
    n_pix = 0 # for debug only
    
    for i in range(w):
        for j in range(h):
            if region[j,i] > 0:
                n_pix += 1
                score += region[j,i]
    #print('Region:')
    #print('Mean: ' + str(score/n_pix), ' / Number of pixels: ' + str(n_pix))
    return score



# Try to find the region with the best 'score'
# Score is based on number of pixels and gray levels.
#
# The tumour is quite large in size and is quite white,
# so we expect the tumour to have the best score
best_region = -1
best_score = 0

# Number of markers on the image
m = markers.max()

for i in range(1, m + 1):
    mask = ws==i
    score = compute_score(brain_img*mask, im_w, im_h)
    if score > best_score:
        best_region = i
        best_score = score

print('Best region:', best_region)
print('Best score:', best_score)
print('Please see results BELOW')
mask = (ws==best_region)

# Show the result
plt.figure(figsize=(20,10))
plt.subplot(1,3,1)
plt.imshow(gradient_i, cmap=plt.cm.gray)
plt.subplot(1,3,2)
plt.imshow(mark_boundaries(brain_img,ws))
plt.subplot(1,3,3)
plt.imshow(brain_img*mask,cmap=plt.cm.gray)
plt.show()



# Area in cm² of ONE pixel
pix_area = 0.115*0.115



### FINAL RESULT ###
print("\n\n--- RESULTS ---\n")
print("Estimated area:", mask.sum() * pix_area, 'cm²')
plt.figure()
plt.imshow(mask * 255,cmap=plt.cm.gray)
plt.show()