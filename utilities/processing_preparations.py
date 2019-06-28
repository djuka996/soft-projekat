from utilities import masking_utilities as pp
from utilities import image_utilites as iu
from utilities import color_utilities as cd
from model import boundaries_pair as bp
import colorsys as cs


def get_game_attributes(image):
    # Get the bounds of the table color
    table_bounds = get_hsv_table_color_bounds(image)
    # Get the table dimensions
    dimensions = pp.get_table_dimensions(image, table_bounds.lower_bounds, table_bounds.upper_bounds)
    # Crop the image for faster processing
    cropped_image = pp.crop_full_image_to_table(image, dimensions)
    # Get the mask of the table, including the balls on it
    table_mask_with_balls = pp.get_mask_full_table(cropped_image,
                                                   table_bounds.lower_bounds,
                                                   table_bounds.upper_bounds)
    # Get the mask of the table, without the balls on it
    table_mask_without_balls = pp.get_mask_table_without_balls(cropped_image,
                                                               table_bounds.lower_bounds,
                                                               table_bounds.upper_bounds)
    # Get only the balls from the cropped image, so Hough circles has a limited search
    result = pp.get_balls_on_table(cropped_image, table_mask_with_balls, table_mask_without_balls)
    # Calculate the average radius
    average_radius = iu.get_average_radius(result)
    return table_bounds, dimensions, average_radius


def get_hsv_table_color_bounds(image):
    # Get the RGB color of the table
    table_color_rgb = cd.get_table_color(image)
    # Convert the RGB color to HSV color space
    table_color_conversion = cs.rgb_to_hsv(table_color_rgb[0], table_color_rgb[1], table_color_rgb[2])
    # Convert it to Python's HSV values
    table_color_hsv = [table_color_conversion[0]*180, table_color_conversion[1]*255, table_color_conversion[2]]
    # Make the bounds based on extracted color and return it
    table_bounds = bp.BoundariesPair([table_color_hsv[0]-10, table_color_hsv[1]-50, 0],
                                     [table_color_hsv[0]+10, 255, 255])
    return table_bounds
