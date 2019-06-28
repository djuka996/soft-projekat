import numpy as np
import cv2


def get_mask_in_range(image, lower_array, upper_array):
    # Convert image to HSV color space
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Get color ranges
    lower_color_range = np.array(lower_array)
    upper_color_range = np.array(upper_array)
    # Extract the mask and return it
    local_mask = cv2.inRange(image_hsv, lower_color_range, upper_color_range)
    return local_mask


def remove_range_from_image(image, lower_array, upper_array):
    # Convert image to HSV color space
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Get color ranges
    lower_color_range = np.array(lower_array)
    upper_color_range = np.array(upper_array)
    # Extract the mask
    local_mask = cv2.inRange(image_hsv, lower_color_range, upper_color_range)
    # Inverse the mask
    local_mask = cv2.bitwise_not(local_mask)
    transformed_image = cv2.bitwise_and(image, image, mask=local_mask)
    return transformed_image


def get_circles_on_image(original_image, average_radius):
    # Convert image to gray scale
    gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # Distance of centers is close to average radius
    centers_distance = np.uint16(np.floor(average_radius))
    # Minimum and maximum radii are 70% and 120% of the average radius
    min_radius = np.uint16(np.around(average_radius*0.7))
    max_radius = np.uint16(np.around(average_radius*1.2))
    # Get circles via Hough circles transformation
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, centers_distance*0.6, param1=25, param2=10,
                               minRadius=min_radius,
                               maxRadius=max_radius)
    if circles is None:
        return None
    # Round the circles
    circles = np.uint16(np.around(circles))
    return circles


def get_ball_mask(image, lower_array, upper_array):
    # Get mask of pixels that are in given range
    mask = get_mask_in_range(image, lower_array, upper_array)
    # Transform the mask so it's wider than the balls and return it
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=3)
    mask = cv2.dilate(mask, kernel, iterations=8)
    return mask


def get_average_radius(image_with_only_balls):
    # Convert image to gray scale
    temp_image = cv2.cvtColor(image_with_only_balls, cv2.COLOR_BGR2GRAY)
    # Find circles with some wide ranges
    circles = cv2.HoughCircles(temp_image, cv2.HOUGH_GRADIENT, 1, 16, param1=35, param2=10, minRadius=6, maxRadius=20)
    circles = np.uint16(np.around(circles))
    # Get the average radius of found circles - that should be the average radius of the ball ( not the noises )
    average_radius = np.uint16(np.around((np.average(circles, axis=1)[0])[2]))
    return average_radius


def mark_circles_on_image(image, circles):
    if circles is None:
        return image
    temp_image = image.copy()
    for i in circles[0, :]:
        cv2.circle(temp_image, (i[0], i[1]), i[2], (0, 255, 0), 2)
    return temp_image


def get_cropped_ball_image(image, circle):
    # Constant factor for image
    factor = 0.7
    # Get coordinates in local variables
    center_x = circle[0]
    center_y = circle[1]
    radius = circle[2]
    # Widen the rectangle for a small amount
    extreme_left = int(center_x - radius * factor)
    extreme_right = int(center_x + radius * factor)
    extreme_top = int(center_y - radius * (factor + 0.2))
    extreme_bottom = int(center_y + radius * factor)
    # Crop the image and return it
    result = image[extreme_top:extreme_bottom, extreme_left:extreme_right]
    return result
