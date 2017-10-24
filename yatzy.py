# This is a yatzy game created to learn python

import sys; print(sys.version)
import logging
from score_card import *
from dice import *
from collections import Counter

logging.basicConfig(filename="yatzy.log",
                    level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")

def play_yatzy():
    print("Welcome to Henrik's Yatzy game.\n")
    my_score_card = Score_card(1)
    my_score_card.print_card()
    while my_score_card.rounds_left != 0:
        start_round(my_score_card)
        my_score_card.print_card()
    print("Game over. Your final score is X")

def start_round(score_card):
    #takes a score_card object as argument and returns it updates it with the round's result
    dice_list = []
    attempts = 3
    round_done = False
    for x in range(5):
        dice_list.append(Dice(6))
    for x in range(attempts):
        print("\nThrow " + str(x+1) + " of " +str(attempts) + ":")
        for y in range(len(dice_list)):
            if dice_list[y].keep == False:
                dice_list[y].roll_dice()
            print(("Dice " + str(y+1)) + ": " + str(dice_list[y].value))
        if x == (attempts - 1): #The user does not need to tell us what dices to keep the attempt
            for y in range(len(dice_list)): # Not really needed to assign keep = True to all dices but may be handy later on
                dice_list[y].keep = True
            break
        valid_input = False
        while valid_input == False:
            user_input = input("\nWhat dices do you want to keep? Enter the dice number, separated by , (e.g. 1,2,5). If you want to keep none, enter 0 :") # Add validation, including not being able to enter same dice number twice
            for c in user_input:
                if c.isdigit() == True and int(c) <= (len(dice_list) + 1):
                    valid_input = True
                    if int(c) == 0:
                        logging.debug("User entered 0")
                        break
                    dice_no = int(c) - 1
                    dice_list[dice_no].keep = True

            if valid_input == False:
                print("You need enter a valid dice number or 0\n")

    score_card.score_card_try_to_score(dice_list)

play_yatzy()
