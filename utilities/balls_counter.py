import utilities.color_utilities as color_utils
import utilities.image_utilites as image_utils
import utilities.masking_utilities as mask_utils
import model.ball_type as bt
import numpy as np
from model import constant_hsv_ranges
import cv2


def get_balls_list(balls, image) -> list:
    """Returns the list of balls that are present on the image, given the circles which represent them."""
    # Initialize result
    result = []
    cue_ball_position = np.arange(2)
    # Iterate over all balls
    for ball in balls:
        # Crop the ball image
        current_ball_cropped = image_utils.get_cropped_ball_image(image, ball)
        # Get the color of the current ball
        current_ball_color = color_utils.get_ball_color(current_ball_cropped)
        # Add that ball type to the resulting array
        result.append(current_ball_color)
        # If the ball is white, return it's position as well
        if current_ball_color == bt.BallType(0):
            cue_ball_position[0] = ball[0]
            cue_ball_position[1] = ball[1]
    return correct_result(result), cue_ball_position


def correct_result(result: list) -> list:
    """Corrects the given list of balls decreasing every non-red ball count to 1,
    and increasing the red ball count accordingly"""
    # Instantiate new result
    new_result = []
    # Count occurrence of each color
    current_state = [[x, result.count(x)] for x in set(result)]
    # Count number of reds to add
    reds_missing = 0
    # If it's not red ball and it appears more than once, correct it
    for element in current_state:
        if element[0] != bt.BallType.RED and element[1] > 1:
            reds_missing += element[1] - 1
            element[1] = 1
        if element[0] == bt.BallType.RED:
            new_result.extend([element[0] for i in range(element[1] + reds_missing)])
        else:
            new_result.extend([element[0] for i in range(element[1])])
    return new_result


def get_differences(state_1: list, state_2: list) -> set:
    """Returns the difference of two given collections."""
    return set(state_1).symmetric_difference(state_2)


def get_balls_on_image(current_image, table_bounds, average_radius):
    """Returns list of circle centers that represent balls on given image."""
    # Create the constants holder
    gc = constant_hsv_ranges.GlobalConstants()
    # Array that will hold all found balls ( circles )
    balls_by_clustering = []
    # Extract full table mask
    full_table_mask = mask_utils.get_mask_full_table(current_image, table_bounds.lower_bounds, table_bounds.upper_bounds)
    # Prepare the image for analysis
    prepared_image = cv2.bitwise_and(current_image, current_image, mask=full_table_mask)
    # Iterate over predefined color ranges
    for current_bounds in gc.bounds[:8]:
        # Extract the mask on prepared image that corresponds to the current color range
        current_mask = image_utils.get_ball_mask(prepared_image, current_bounds.lower_bounds, current_bounds.upper_bounds)
        # Get those parts on the prepared image
        current_balls = cv2.bitwise_and(prepared_image, prepared_image, mask=current_mask)
        # Extract circles from the extracted ball
        found_circles = image_utils.get_circles_on_image(current_balls, average_radius)
        if found_circles is not None:
            balls_by_clustering.extend(np.array(found_circles[0, :]))
    return balls_by_clustering
