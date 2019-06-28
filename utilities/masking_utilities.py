import cv2
import numpy as np
from utilities import image_utilites as iu
import imutils


def get_mask_table_without_balls(original_image, table_lower, table_upper):
    # Get the table mask with original clarity
    table_mask = iu.get_mask_in_range(original_image, table_lower, table_upper)
    # Make kernel for dealing with noises
    table_kernel = np.ones((5, 5), np.uint8)
    # Fix mask using the kernel
    table_mask = cv2.erode(table_mask, table_kernel, iterations=2)
    table_mask = cv2.dilate(table_mask, table_kernel, iterations=2)
    table_mask = cv2.erode(table_mask, table_kernel, iterations=5)
    return table_mask


def get_mask_full_table(original_image, table_lower, table_upper):
    # Get table mask without balls
    table_mask = get_mask_table_without_balls(original_image, table_lower, table_upper)
    # Find contours on image
    contours = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    # Get the largest contour ( assumption that's the table )
    c = max(contours, key=cv2.contourArea)
    # Approximate the contour to be a convex hull ( for a straighter shape )
    approximated_contour = cv2.convexHull(c)
    # Resize the contour because of top cushion
    approximated_contour[:, :, 0] = approximated_contour[:, :, 0] * 1
    approximated_contour[:, :, 1] = approximated_contour[:, :, 1] * 0.9
    # Draw and fill calculated contour
    table_mask = cv2.drawContours(table_mask, [approximated_contour], -1, (255, 255, 255), -1)
    return table_mask


def get_table_dimensions(original_image, table_lower, table_upper):
    # Get table mask without balls
    table_mask = get_mask_table_without_balls(original_image, table_lower, table_upper)
    # Find contours on image
    contours = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    # Get the largest contour ( assumption that's the table )
    c = max(contours, key=cv2.contourArea)
    # Get extreme points of contour
    ext_left = tuple(c[c[:, :, 0].argmin()][0])[0]
    ext_right = tuple(c[c[:, :, 0].argmax()][0])[0]
    ext_top = tuple(c[c[:, :, 1].argmin()][0])[1]
    ext_bot = tuple(c[c[:, :, 1].argmax()][0])[1]
    # Return extreme coordinates
    return [ext_left, ext_right, ext_top, ext_bot]


def crop_full_image_to_table(original_image, dimensions):
    # Extract dimensions into variables
    ext_top = int(dimensions[2] * 0.6)
    ext_bot = int(dimensions[3] * 1.05)
    ext_left = dimensions[0]
    ext_right = dimensions[1]
    # Crop the image to calculated dimension
    cropped_image = original_image[ext_top:ext_bot, ext_left:ext_right]
    return cropped_image


def get_balls_on_table(cropped_image, table_mask_with_balls, table_mask_without_balls):
    # Morphological transformations to get only the ( areas around ) balls as positives on mask
    result = cv2.bitwise_not(table_mask_without_balls, table_mask_without_balls, mask=table_mask_with_balls)
    result = cv2.erode(result, kernel=np.ones((5, 5), np.uint8), iterations=6)
    result = cv2.dilate(result, kernel=np.ones((5, 5), np.uint8), iterations=2)
    result = cv2.bitwise_and(result, result, mask=table_mask_with_balls)
    # Extract colored balls on the given cropped image
    result = cv2.bitwise_and(cropped_image, cropped_image, mask=result)
    return result
