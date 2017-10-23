from collections import Counter
import score_card
import dice

l = [1,2,3,2,3,3,3,2,2,1,2]

my_score_card = score_card.Score_card(1)
dice_list = []
for x in range(5):
    dice_list.append(dice.Dice(6))
    #dice_list[x].roll_dice()
    dice_list[x].print_dice()

dice_list[0].value = 2
dice_list[1].value = 2
dice_list[2].value = 4
dice_list[3].value = 6
dice_list[4].value = 6

my_score_card.score_card_try_to_score(dice_list)
my_score_card.print_card()
