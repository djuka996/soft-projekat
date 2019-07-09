import cv2
import utilities.processing_preparations as processing_utils
import utilities.masking_utilities as mask_utils
import utilities.balls_counter as counter
import utilities.image_utilites as image_utils
import model.points_logic as logic
import model.ball_type as bt
import math
import numpy as np


def calculate_distance(position1, position2):
    distance = math.sqrt(math.pow(position1[0] - position2[0], 2) +
                         math.pow(position1[1] - position2[1], 2))
    # print(distance)
    return distance


def get_contacted_ball(cropped_previous_frame, cropped_current_frame):
    temporary_table_mask = mask_utils.get_mask_full_table(cropped_current_frame,
                                                          table_bounds.lower_bounds,
                                                          table_bounds.upper_bounds)
    cropped_previous_frame_gray = cv2.cvtColor(cropped_previous_frame, cv2.COLOR_BGR2GRAY)
    cropped_current_frame_gray = cv2.cvtColor(cropped_current_frame, cv2.COLOR_BGR2GRAY)
    frames_difference_mask = cv2.absdiff(cropped_current_frame_gray, cropped_previous_frame_gray)
    frames_difference = cv2.bitwise_and(cropped_current_frame, cropped_current_frame, mask=frames_difference_mask)
    cleared_image = image_utils.remove_range_from_image(frames_difference,
                                                        table_bounds.lower_bounds,
                                                        table_bounds.upper_bounds)
    cleared_image = cv2.bitwise_and(cleared_image, cleared_image, mask=temporary_table_mask)
    kernel = np.ones((3, 3), np.uint8)
    cleared_image = cv2.erode(cleared_image, kernel, iterations=5)
    cleared_image = cv2.dilate(cleared_image, kernel, iterations=5)
    found_circles = image_utils.get_circles_on_image(cleared_image, average_radius)
    first_hit_ball = None
    if found_circles is not None:
        circles_of_interest = []
        for circle in found_circles[0, :]:
            circles_of_interest.extend([circle])
        balls_that_moved, _ = counter.get_balls_list(circles_of_interest, cropped_current_frame)
        # print_balls(balls_that_moved)
        balls_that_moved.remove(bt.BallType(0))
        if balls_that_moved:
            first_hit_ball = balls_that_moved[0]
    # cv2.imshow("Frame difference", cleared_image)
    # cv2.waitKey(1)
    return first_hit_ball


def print_balls(result):
    print([[x, result.count(x)] for x in set(result)])


# Učitavanje video snimka
video_file = "C:\\Users\\Aleksa\\Videos\\Captures\\PLAVA_KUGLA_REGULARNO_2.mp4"
video = cv2.VideoCapture(video_file)
frames_to_skip = 10
should_aim_red = False
# Računanje atributa partije - dimenzije kugli, boje stola, dimenzije stola
success, first_frame = video.read()
table_bounds, dimensions, average_radius = processing_utils.get_game_attributes(first_frame)
# Postavka pomoćnih promenljivih
cropped_previous_frame = None
contacted_ball = None
current_frame_number = 0
previous_cue_ball_position = None
moving = False
in_motion = False
minimum_distance = 15
error_distance = 40
iterator = 0
text = "NO"
# Iteriranje kroz snimak
while video.isOpened():
    # Iščitaj frejm
    success, current_frame = video.read()
    if success:
        # Iščitani frejm
        cropped_current_frame = mask_utils.crop_full_image_to_table(current_frame, dimensions)
        # Preuzmi krugove sa iščitanog frejma
        balls = counter.get_balls_on_image(cropped_current_frame, table_bounds, average_radius)
        # Pronađi kugle i poziciju bele kugle
        result, current_cue_ball_position = counter.get_balls_list(balls, cropped_current_frame)
        # Postavi prethodni frejm i prethodnu poziciju bele kugle
        if cropped_previous_frame is None and previous_cue_ball_position is None:
            cropped_previous_frame = cropped_current_frame
            previous_cue_ball_position = current_cue_ball_position
        # print_balls(result)
        current_distance = calculate_distance(previous_cue_ball_position, current_cue_ball_position)
        # Ako je bela pomerena dovoljno, registruj kretanje
        if current_distance < minimum_distance:
            moving = False
            text = "NO"
        else:
            moving = True
            text = "YES"
            # Pošto je u pokretu i nije napravljen kontakt ni sa jednom kuglom, probaj da ga nađeš
            if contacted_ball is None:
                contacted_ball = get_contacted_ball(cropped_previous_frame, cropped_current_frame)
        if in_motion is False and moving is True:
            # Početak kretanja bele kugle
            in_motion = True
            # Sačuvaj listu kugli kao početno stanje
            begin_state = result
        if in_motion is True and moving is False:
            # Završetak kretanja bele kugle
            in_motion = False
            # Sačuvaj listu kugli kao krajno stanje
            end_state = result
            # Isprocesiraj informacije i izgeneriši rezultat
            balls_difference = counter.get_differences(begin_state, end_state)
            result = logic.get_points_for_shot(list(balls_difference), contacted_ball, should_aim_red)
            print("Points: " + str(result))
        cv2.putText(cropped_current_frame, "BALL IN MOTION: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow("Snimak", cropped_current_frame)
        cv2.waitKey(1)
        # Preskakanje frejmova i postavka promenljivih
        current_frame_number += frames_to_skip
        iterator += 1
        video.set(1, current_frame_number)
        previous_cue_ball_position = current_cue_ball_position
        cropped_previous_frame = cropped_current_frame
    else:
        video.release()
        break
