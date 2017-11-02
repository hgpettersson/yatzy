import logging
from dice import *
from collections import Counter

logging.basicConfig(filename="yatzy.log",
                    level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")

class Score_card(object):

    def __init__(self, player_name):
        self.rounds_played = 0
        self.score_card_top_section_sum = 0
        self.score_card_top_section_bonus = 0
        self.score_card_total_sum = 0
        self.score_card_top_section = []
        self.score_card_bottom_section = []
        self.player_name = player_name
        for x in range(6):
            self.score_card_top_section.append(Score_card_category_top_section(x+1))
        self.score_card_bottom_section.append(Score_card_category_multiples(2, "Pair"))
        self.score_card_bottom_section.append(Score_card_category_two_pairs())
        self.score_card_bottom_section.append(Score_card_category_multiples(3, "Three of a kind"))
        self.score_card_bottom_section.append(Score_card_category_multiples(4, "Four of a kind"))
        self.score_card_bottom_section.append(Score_card_category_full_house())
        self.score_card_bottom_section.append(Score_card_category_straight(1, 5, "Small straight"))
        self.score_card_bottom_section.append(Score_card_category_straight(2, 6, "Large straight"))
        self.score_card_bottom_section.append(Score_card_category_chance("Chance"))
        self.score_card_bottom_section.append(Score_card_category_multiples(5, "Yatzy"))
        self.rounds_left = len(self.score_card_top_section) + len(self.score_card_bottom_section) - self.rounds_played

    def print_card(self):
        self.score_card_sum()
        self.rounds_left = len(self.score_card_top_section) + len(self.score_card_bottom_section) - self.rounds_played
        for x in self.score_card_top_section:
            scratched_string = ""
            if x.scratched == True:
                scratched_string = "(Scracthed)"
            print(x.description + ": " + str(x.score) + scratched_string)
        print("Sum: " + str(self.score_card_top_section_sum) + "\n"
                + "Bonus: " + str(self.score_card_top_section_bonus) +"\n")
        for x in self.score_card_bottom_section:
            scratched_string = ""
            if x.scratched == True:
                scratched_string = "(Scratched)"
            print(x.description + ": " + str(x. score)+ scratched_string)
        print("Total sum: " + str(self.score_card_total_sum))

    def score_card_sum(self):
        self.score_card_top_section_sum = 0
        self.score_card_bottom_section_sum = 0
        self.score_card_total_sum = 0

        for x in self.score_card_top_section:
            self.score_card_top_section_sum = self.score_card_top_section_sum + x.score
        if self.score_card_top_section_sum > 63:
            self.score_card_top_section_bonus = 50
        for x in self.score_card_bottom_section:
            self.score_card_bottom_section_sum = self.score_card_bottom_section_sum + x.score
        self.score_card_total_sum = self.score_card_top_section_sum + self.score_card_top_section_bonus + self.score_card_bottom_section_sum

    def score_card_try_to_score(self, dice_list):
        #accepts a list of dices as input. Need to add logic to handle user choosing a non-valid category, that is the category class method try_to_score returns False.
        while True:
            valid_category_entered = False # Need this control variable as try_to_score() also can require reentry of category, e.g. if category is already chosen
            user_input = input("Choose a category: ")
            for x in self.score_card_top_section:
                if x.description == user_input:
                    valid_category_entered = True
                    if x.try_to_score(dice_list):
                        self.rounds_played = self.rounds_played + 1
                        self.score_card_sum()
                        return

            for x in self.score_card_bottom_section:
                if x.description == user_input:
                    valid_category_entered = True
                    if x.try_to_score(dice_list):
                        self.rounds_played = self.rounds_played + 1
                        self.score_card_sum
                        return
            if valid_category_entered == False:
                print("You did not enter a valid category. Try again")


class Score_card_category(object):

    def __init__(self):
        self.empty = True
        self.score = 0
        self.scratched = False
        self.description = ""

    def try_to_score(self, dices):
    # accepts a list of dices as input. Returns the score if successful, else False.
        if self.score > 0:
            print("You have already scored " + self.description)
            return False

        if self.scratched == True:
            print("You have already scratched " + self.description)
            return False

    def scratch_category(self):
        # Asks users whether she wants to scratch the category. Updates scratched variable and returns True or False.

        while True:
            user_input = input("Do you want to scatch " + self.description + " ? (Y/N)")
            if user_input == "Y":
                self.scratched = True
                return True
            elif user_input == "N":
                return False
            else:
                print("Bad input. Please enter Y or N. ")

class Score_card_category_top_section(Score_card_category):
    def __init__(self, number):
        #number refers to 1-6
        Score_card_category.__init__(self)
        self.number = number
        self.description = str(number) + "s"

    def try_to_score(self, dices):
    # accepts a list of dices as input. Updates score if successful and returns True, else retruns False.
        if super().try_to_score(dices) == False: # DONT UNDERSTAND WHY I NEED TO DO IT LIKE THIS. WHY CANT THE SUPER CLASS METHOD JUST RETURN FALSE?
            return False
        for x in range(len(dices)):
            if self.number == dices[x].value:
                self.score = self.score + self.number
        if self.score > 0:
            return True
        else:
            print("You had no " + str(self.number) + "s")
            if super().scratch_category():
                return True # The round counter should be incremented if a player scratches a category
            else:
                return False

class Score_card_category_multiples(Score_card_category):
    #This class is used to create the pair, three of a kind, four of a kind and yatzy (five of a kind).
    def __init__(self, multiple, description):
        Score_card_category.__init__(self)
        self.description = description
        self.multiple = multiple

    def try_to_score(self, dices):
        #Improvement idea: Have try to score accept a dice number that it should try, rather than asking the user what number to go for if there are several multiples among the dice. This will make it more general and easier to reuse with the two pairs class.
        if super().try_to_score(dices) == False:
            return False

        dice_values_list = []
        for x in dices:
            dice_values_list.append(x.value)

        c = Counter(dice_values_list)
        logging.debug("this is the value of Counter c: " + str(c))
        multiples = []
        for key, value in c.items():
            if value >= self.multiple:
                multiples.append(key)

        logging.debug("this is the value of the multiples list: " + str(multiples))

        if len(multiples) > 0 and self.multiple == 5:
            self.score = 50
            print("You scored Yatzy you fu**er! \n")
            return True

        elif len(multiples) > 1:
            alternatives = "Please choose between "
            for x in multiples:
                alternatives = alternatives + str(x) + "s, "
            alternatives = alternatives + " (e.g. 1s, 2s etc)."
            user_input = input(alternatives) #validation needed
            user_input = user_input[0]
            logging.debug("Remaining user_input: " + str(user_input))
            logging.debug("self.multiple: " + str(self.multiple))
            self.score = self.multiple * int(user_input)
            return True

        elif len(multiples) == 1:
            self.score = multiples[0]* self.multiple
            return True

        else:
            #if there are no multiples
            print("There are no " + str(self.description))
            if super().scratch_category():
                return True # The round counter should be incremented if a player scratches a category
            else:
                return False

class Score_card_category_two_pairs(Score_card_category):
    def __init__(self):
        Score_card_category.__init__(self)
        self.description = "Two pairs"


    def try_to_score(self, dices):
        # Reuses the Multpiples class

        if super().try_to_score(dices) == False:
            return False

        Pair1 = Score_card_category_multiples(2, "Pair1")
        Pair2 = Score_card_category_multiples(2, "Pair2")

        if Pair1.try_to_score(dices):
            for x in dices:
                logging.debug("x in dices: " + str(x))
                logging.debug("index of x in dices: " + str(dices.index(x)))
                if x.value == Pair1.score / 2:
                    dices.pop(dices.index(x))

            if Pair2.try_to_score(dices):
                self.score = Pair1.score + Pair2.score
                return True
            else:
                print("You only rolled one pair")
                return False
        else:
            print("You rolled no pairs")
            if super().scratch_category():
                return True # The round counter should be incremented if a player scratches a category
            else:
                return False

class Score_card_category_straight(Score_card_category):

    def __init__(self, straight_start, straight_end, description):
        Score_card_category.__init__(self)
        self.straight_start = straight_start
        self.straight_end = straight_end
        self.description = description

    def try_to_score(self, dices):
        if super().try_to_score(self) == False:
            return False

        dice_values_list = []
        for x in dices:
            dice_values_list.append(x.value)

        dice_values_list.sort()

        if dice_values_list[0] == self.straight_start:
            dice_values_list_index = 1
            while dice_values_list_index < len(dice_values_list) - 1:
                if dice_values_list[dice_values_list_index] == dice_values_list[dice_values_list_index - 1] + 1:
                    dice_values_list_index = dice_values_list_index + 1
                else:
                    print("You do not have a " + self.description)
                    return False

            self.score = sum(dice_values_list)
            return True

        else:
            print("You do not have a " + self.description)
            if super().scratch_category():
                return True # The round counter should be incremented if a player scratches a category
            else:
                return False

class Score_card_category_chance(Score_card_category):
# Chance category can never be scratched
    def __init__(self, description):
        Score_card_category.__init__(self)
        self.description = description

    def try_to_score(self, dices):
        if super().try_to_score(self) == False:
            return False

        for x in dices:
            self.score = self.score + x.value

        return True

class Score_card_category_full_house(Score_card_category):

    def __init__(self):
        Score_card_category.__init__(self)
        self.description = "Full house"

    def try_to_score(self, dices):

        if super().try_to_score(self) == False:
            return False

        dice_values_list = []
        for x in dices:
            dice_values_list.append(x.value)

        c = Counter(dice_values_list)
        logging.debug("Multiples counter, full house category: " + str(c))
        logging.debug("Value of c[0]: " + str(c[0]))

        used_dices = 0
        for key, value in c.items():
            logging.debug("key: " + str(key) + "value: " + str(value) + "used_dices: " + str(used_dices))
            if value > 1:
                used_dices = used_dices + value
                self.score = self.score + key * value

        if used_dices == 5:
            return True
        else:
            self.score = 0
            print("You do not have a full house")
            return False
