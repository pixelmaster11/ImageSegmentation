import cv2
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum

'''
This functions loads the image and corrects its colors as provided
'''
def load_image(filepath, grayscale = False, toRGB = True):

    img = cv2.imread(filepath)

    if grayscale:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    elif toRGB:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    return img

'''
This functions displays the image using matplotlib
'''
def display_image(img, cmap = None):
    fig = plt.figure(figsize=(10,10), facecolor="gray")
    ax = fig.add_subplot(1,1,1)
    ax.imshow(img, cmap=cmap)
    plt.show()


'''
This functions resizes given image based on percent and preserving aspect ratio if required
'''
def resize_image(img, scale = 0.6, preserveAspect = True , width = 500, height = 500):

    if preserveAspect:
        width = int(img.shape[1] * scale)
        height = int(img.shape[0] * scale)

    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    return resized