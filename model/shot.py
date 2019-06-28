import utilities.balls_counter as bc


class Shot:
    def __init__(self, starting_balls, finishing_balls, first_contact, aims_red):
        # Ball situation prior to the shot
        self.starting_balls = starting_balls
        # Ball situation after shot
        self.finishing_balls = finishing_balls
        # First ball hit
        self.first_contact = first_contact
        # Boolean variable declaring whether or not the player has to aim at red ball
        self.aims_red = aims_red

    def log_print(self):
        return " hit the " + self.first_contact.name + " and the balls difference is " + \
               str([ball.name for ball in bc.get_differences(self.starting_balls, self.finishing_balls)])
