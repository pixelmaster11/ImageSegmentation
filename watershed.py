from img_tools import load_image, resize_image
import os
import cv2
import numpy as np
from matplotlib import cm

'''
Create rgb values from colormap
'''
def create_rgb(i):

    #x = np.array(cm.colors.to_rgb(cm.colors.CSS4_COLORS[i])) * 255
    x = np.array(cm.tab10(i)[:3]) * 255
    return tuple(x)

'''
Define the mouse callback
'''
def mouse_callback(event, x, y, flags, param):
    global marks_updated, current_marker, img_copy

    if event == cv2.EVENT_LBUTTONDOWN:

        print(current_marker)

        # TRACKING FOR MARKERS
        cv2.circle(marker_image, (x, y), 10, (current_marker), -1)

        # DISPLAY ON USER IMAGE
        cv2.circle(img_copy, (x, y), 10, colors[current_marker], -1)
        marks_updated = True

'''
Apply watershed algorithm
'''
def interactive_watershed():

    global segments, img_copy, marks_updated, marker_image, current_marker

    # One color for each single digit

    for i in range(n_markers):
        colors.append(create_rgb(i))

    # Assign callbacks
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', mouse_callback)

    while True:

        # SHow the 2 windows
        cv2.imshow('Segments', segments)
        cv2.imshow('Image', img_copy)


        # Close everything if Esc is pressed
        k = cv2.waitKey(1)
        if k == 27:
            break

        # Clear all colors and start over if 'c' is pressed
        elif k == ord('c'):
            img_copy = img.copy()
            marker_image = np.zeros(img.shape[0:2], dtype=np.int32)
            segments = np.zeros(img.shape, dtype=np.uint8)
            current_marker = 1

        # If a number 0-9 is chosen index the color
        elif k > 0 and chr(k).isdigit():
            # chr converts to printable digit

            current_marker = int(chr(k))

        # If we clicked somewhere, call the watershed algorithm on our chosen markers
        if marks_updated:

            marker_image_copy = marker_image.copy()
            cv2.watershed(img, marker_image_copy)

            segments = np.zeros(img.shape, dtype=np.uint8)

            for color_ind in range(n_markers):
                segments[marker_image_copy == (color_ind)] = colors[color_ind]

            marks_updated = False

    cv2.destroyAllWindows()



if __name__ == '__main__':

    # Path to image
    path = "ac1.jpg"

    # Load image
    img = load_image(path, toRGB=False)

    # Resize image
    img = resize_image(img, preserveAspect=True, scale=0.8)

    # Manip on image copy
    img_copy = img.copy()


    #Placeholders for marker and segments
    marker_image = np.zeros(img.shape[:2], dtype=np.int32)
    segments = np.zeros(img.shape, dtype=np.uint8)

    #Total markers to be used for segmenting (Single digits 0-9)
    n_markers = 10

    #Curently active marker
    current_marker = 1

    #Check whether marker has been updated / drawn
    marks_updated = False

    #List to hold marker/segment colors
    colors = []

    interactive_watershed()

