from model import ball_type as bt


def get_points_for_shot(balls_difference, first_contact, aims_red):
    # If the player has failed to hit a ball
    if first_contact is None:
        return -4
    # If the player should shoot at red balls
    if aims_red:
        # And he contacted red first
        if first_contact == bt.BallType.RED:
            # If there is no difference, then no balls have been potted, but it's a legal shot
            if len(balls_difference) == 0:
                return 0
            # If only red balls are missing, it's a legal shot
            if all(ball == bt.BallType.RED for ball in balls_difference) and len(balls_difference) > 0:
                # Award 1 point for each potted red
                return len(balls_difference)
            # If he potted any other ball
            else:
                # Foul at least 4 points, or more if he first hit a higher valued ball
                return -1*max(get_highest_valued_color(balls_difference), 4)
        # But he didn't contact red first ( and we know he made contact )
        else:
            # Foul at least 4 points, or more if he first hit a higher valued ball
            return -1*max(first_contact.value, 4)
    # If the player should shoot at "colored" balls
    else:
        # And he contacted "colored" ball first
        if first_contact != bt.BallType.RED:
            # If there is no difference, then no balls have been potted, but it's a legal shot
            if len(balls_difference) == 0:
                return 0
            # If the balls are different by more than one, it's a foul certainly
            if len(balls_difference) > 1:
                # Foul is at least 4 points, or more if he first hit a higher valued ball
                return -1*max(first_contact.value, 4)
            # He potted one ball, we need to check which one
            else:
                # If he potted the one he hit first, it's a legal shot
                if balls_difference[0] == first_contact:
                    # Award points to the player
                    return first_contact.value
                else:
                    # Foul is at least 4 points, or more if he first hit a higher valued ball
                    return -1 * max(get_highest_valued_color(balls_difference), 4)
        # Award points to the opposing player
        else:
            # Foul is 4 or more points - but that can't be decided based on video only ( he needs to call the ball )
            return -4


def get_highest_valued_color(balls):
    # Get the highest valued color that he hit
    max_points = 0
    # Iterate over all balls and get the highest one
    for ball in balls:
        if ball.value > max_points:
            max_points = ball.value
    return max_points
