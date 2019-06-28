import cv2
import utilities.processing_preparations as pp
import utilities.balls_counter as counter
import utilities.masking_utilities as mask_utils


# Preuzimanje slike
image_file_location1 = "C:\\Users\\Aleksa\\Documents\\soft\\novi_snimak_snap.jpg"
image = cv2.imread(image_file_location1)
# Izračunavanje atributa partije
table_bounds, dimensions, average_radius = pp.get_game_attributes(image)
# Kropovanje slike
cropped_image = mask_utils.crop_full_image_to_table(image, dimensions)
# Preuzimanje liste trenutnih kugli sa slike
balls = counter.get_balls_on_image(cropped_image, table_bounds, average_radius)
result = counter.get_balls_list(balls, cropped_image)
print([[x, result.count(x)] for x in set(result)])
cv2.imshow("Image", image)
cv2.waitKey(0)
