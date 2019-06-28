import colorsys as cs
from skimage import color
import cv2
from sklearn.cluster import KMeans
import math
from model import ball_type as bt, colors_lab_space as cls
import numpy as np


def get_table_color(image):
    # Convert image to RGB color space
    local_image = image.copy()
    # Get half the width and height
    width = int(local_image.shape[1] * 0.3)
    height = int(local_image.shape[0] * 0.3)
    dim = (width, height)
    # Resize the image and convert it to gray scale
    local_image = cv2.resize(local_image, dim, interpolation=cv2.INTER_AREA)
    local_image = cv2.cvtColor(local_image, cv2.COLOR_BGR2RGB)
    local_image = local_image.reshape((local_image.shape[0] * local_image.shape[1], 3))
    # Cluster it using KMeans into 2 clusters - one for the ( presumably ) green of the cloth, and other for shadows
    clt = KMeans(n_clusters=2)
    clt.fit(local_image)
    # Return greener of the two colors
    return get_greener_color(clt.cluster_centers_)


def get_greener_color(colors):
    # Approximated green color in HSV space
    green = [50, 200, 140]
    # If the color is close enough, return it
    for current_color in colors:
        hsv = cs.rgb_to_hsv(current_color[0], current_color[1], current_color[2])
        if abs(hsv[0]*180 - green[0]) < 20:
            return current_color
    return None


def convert_rgb_to_lab(rgb):
    rgb_color = [[[rgb[0]/255, rgb[1]/255, rgb[2]/255]]]  # Note the three pairs of brackets
    lab_color = color.rgb2lab(rgb_color)
    return lab_color[0][0]


def get_ball_color(image):
    # Convert to RGB color space
    local_image = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
    local_image = local_image.reshape((local_image.shape[0] * local_image.shape[1], 3))
    # Cluster it using KMeans into 2 clusters:
    clt = KMeans(n_clusters=2, n_init=40)
    clt.fit(local_image)
    # Get the color of the second cluster by size
    return determine_color_category(get_largest_cluster(clt))


def get_largest_cluster(clt):
    labels = clt.labels_
    _, counts = np.unique(labels, return_counts=True)
    index = np.where(counts == np.amax(counts))
    index = index[0][0]
    return clt.cluster_centers_[index]


def calculate_color_distance(color1, color2):
    return math.sqrt(math.pow(color1[0] - color2[0], 2) +
                     math.pow(color1[1] - color2[1], 2) +
                     math.pow(color1[2] - color2[2], 2))


def determine_color_category(source_color):
    # Convert to Lab color space, for easier distance calculation
    source_color_lab = convert_rgb_to_lab(source_color)
    # Instantiate color constants
    constants = cls.GlobalConstants()
    # Prepare variables
    min_distance = None
    result = None
    # Iterate over all predefined colors
    for i, current_color in enumerate(constants.colors):
        # Calculate the current distance
        current_distance = calculate_color_distance(source_color_lab, current_color)
        # Update the result if necessary
        if min_distance is None or min_distance > current_distance:
            min_distance = current_distance
            result = bt.BallType(i)
    return result
