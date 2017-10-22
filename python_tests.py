from collections import Counter
import score_card
import dice

l = [1,2,3,2,3,3,3,2,2,1,2]

my_score_card = score_card.Score_card(1)
dice_list = []
for x in range(5):
    dice_list.append(dice.Dice(6))
    dice_list[x].roll_dice()
    #dice_list[x].value = 2
    dice_list[x].print_dice()

my_score_card.score_card_try_to_score(dice_list)
my_score_card.print_card()

# Next step: Add chance category. Then, test the game with one player
