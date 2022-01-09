

# Imports
from matplotlib import pyplot as plt
from skimage.io import imread, imsave



# Image and watermak paths
path_img = 'img/road.jpg'
path_wat = 'img/watermark.png'





# Files used in this application
img = imread(path_img)
wat = imread(path_wat)

# Store height and width
img_h, img_w = img.shape[0:2]
wat_h, wat_w = wat.shape[0:2]







#  Ask for watermark's location
#
#  The location (0, 0) is assumed to
#  be at the top-left corner of the image

def ask_watermark_location():

    prompt = input("Do you wanna choose the watermark's location? (Y/n)\n").lower()

    if prompt != 'y':
        return (0, 0)   # default location at (0, 0)

    while True:
        try:
            loc_x = int(input("Write the left-margin in px: "))
            loc_y = int(input("Write the top-margin in px: "))

            if loc_x < 0 or loc_y < 0:
                print("No numbers below zero are allowed for the watermark location.\n")
            elif loc_x + wat_w > img_w or loc_y + wat_h > img_h:
                print("The watermark's location is out of bounds.\n")
            else:
                return (loc_x, loc_y)

        except Exception:
            print("Please type integers only.\n")


# Choose the watermak location
loc = ask_watermark_location()









# Add the watermark pixel by pixel

# Float representing the transparency (full opaque = 1, transparent = 0)
alpha = 0.4

# Blank pixel for grayscale images
BLANK_PIXEL = [255]
COLOR = [255, 255, 255]

for i in range(wat_h):
    for j in range(wat_w):
        if wat[i, j] == BLANK_PIXEL:
            curr_loc = (loc[1] + i, loc[0] + j)     # Current location in img
            img[curr_loc][:] = [v + alpha*(COLOR[g] - v) for g, v in enumerate(img[curr_loc])]



# Save a copy of the image
imsave('final_p1.png', img)

