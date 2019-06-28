import cv2
import utilities.processing_preparations as processing_utils
import utilities.masking_utilities as mask_utils
import utilities.balls_counter as counter
import model.points_logic as logic
import math
import numpy as np
import matplotlib.pyplot as plt


def calculate_distance(position1, position2):
    distance = math.sqrt(math.pow(position1[0] - position2[0], 2) +
                         math.pow(position1[1] - position2[1], 2))
    print(distance)
    return distance


def print_dots(x_cue_balls_positions, y_cue_balls_positions):
    plt.scatter(x_cue_balls_positions, y_cue_balls_positions)
    plt.show()


# Učitavanje video snimka
video_file = "C:\\Users\\Aleksa\\Videos\\Captures\\PLAVA_KUGLA_REGULARNO_2.mp4"
video = cv2.VideoCapture(video_file)
frames_to_skip = 10
should_aim_red = False
# Računanje atributa partije - dimenzije kugli, boje stola, dimenzije stola
success, first_frame = video.read()
table_bounds, dimensions, average_radius = processing_utils.get_game_attributes(first_frame)
# Iteriranje kroz snimak
contacted_ball = None
current_frame_number = 0
previous_cue_ball_position = None
moving = False
in_motion = False
minimum_distance = 15
error_distance = 40
x_positions = np.empty(200)
y_positions = np.empty(200)
iterator = 0
while video.isOpened():
    success, current_frame = video.read()
    if success:
        cropped_current_frame = mask_utils.crop_full_image_to_table(current_frame, dimensions)
        balls = counter.get_balls_on_image(cropped_current_frame, table_bounds, average_radius)
        result, current_cue_ball_position = counter.get_balls_list(balls, cropped_current_frame)
        if previous_cue_ball_position is None:
            previous_cue_ball_position = current_cue_ball_position
        current_distance = calculate_distance(previous_cue_ball_position, current_cue_ball_position)
        if current_distance < error_distance:
            x_positions[iterator] = current_cue_ball_position[0]
            y_positions[iterator] = current_cue_ball_position[1]
            cv2.circle(cropped_current_frame, (current_cue_ball_position[0], current_cue_ball_position[1]), 5,
                       (0, 255, 0), -1)
            print([[x, result.count(x)] for x in set(result)])
            cv2.imshow("Current frame", cropped_current_frame)
            cv2.waitKey(0)
        if current_distance < minimum_distance:
            moving = False
        else:
            moving = True
        if in_motion is False and moving is True:
            # Beginning of movement of the cue ball
            in_motion = True
            # Save the list of balls as the begin state
            begin_state = result
        if in_motion is True and moving is False:
            # End of movement of the cue ball
            in_motion = False
            # Save the list of balls as the end state
            end_state = result
            # Process information and calculate points
            balls_difference = counter.get_differences(begin_state, end_state)
            print_dots(x_positions, y_positions)
            # result = logic.get_points_for_shot(balls_difference, contacted_ball, should_aim_red)
            # print("Points: " + result)
        current_frame_number += frames_to_skip
        iterator += 1
        video.set(1, current_frame_number)
        previous_cue_ball_position = current_cue_ball_position
    else:
        video.release()
        break
