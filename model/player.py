class Player:
    def __init__(self, first_name: str, last_name: str, image: str):
        self.first_name = first_name
        self.last_name = last_name
        self.image = image

    def pretty_print(self):
        return self.last_name + " ( " + self.first_name + " )"
