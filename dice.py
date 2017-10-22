import random
import logging

logging.basicConfig(filename="yatzy.log",
                    level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")

class Dice(object):
    keep = False
    value = 0
    def __init__(self, sides):
        self.sides = sides

    def roll_dice(self):
        self.value = random.randint(1,self.sides)
        return self.value

    def print_dice(self):
        print(str(self.value) + ", " + str(self.keep))
