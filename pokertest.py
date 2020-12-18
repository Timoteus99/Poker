import treys
import time
import math
import termcolor


# treys link: https://pypi.org/project/treys/


evaluator = treys.Evaluator()

def what_do_i_got(board, player):
    '''return a string like 'Straight' or 'Flush' '''
    player_score = evaluator.evaluate(board, player)
    player_class = evaluator.get_rank_class(player_score)
    player_string = evaluator.class_to_string(player_class)

    return player_string

def evaluate(hands_list, board):
    '''returns a list of winner like ['player1'] '''
    winners_list = []
    minimum = 7463 #7462 distinct poker handov
    winner = ''
    for hand in hands_list:
        if evaluator.evaluate(board, hand[1]) == minimum:
            winner += ',' + hand[0]
            
        if evaluator.evaluate(board, hand[1]) < minimum:
            minimum = evaluator.evaluate(board, hand[1])
            winner = hand[0]
    #print('Board:' + treys.Card.print_pretty_cards(board))
    # #for element in hands_list:
        #print(element[0] + ' has:' + treys.Card.print_pretty_cards(element[1])) #za lepsi izpis
    #if len(winner) > 7 and len(board) < 5:
        #print(winner + ' are currently spliting!')
    #elif len(winner) > 7:
        #print(winner + ' split the pot!')
    #else:
        #if len(board) < 5:
            #print(winner + ' is currently winning!')
        #else:
            #print(winner + ' wins the pot!')
    if len(winner) > 7:
        winners_list.append(winner.split(',')[0])
        winners_list.append(winner.split(',')[1])
        try:
            winners_list.append(winner.split(',')[2])
            winners_list.append(winner.split(',')[3])
        except:
            pass
    else:
        winners_list.append(winner)

    return winners_list
    
#print(evaluate(hands_list, board))

'''base'''

def random_test(n):
    '''return percentages of winning and hands'''
    results_dict = {'player1' : 0,
                    'player2' : 0,
                    'player3' : 0,
                    'player4' : 0,
                    'player5' : 0,
                    'player6' : 0,
                    'splits' : 0}

    hands_dict = {'High Card' : 0,
                  'Pair' : 0,
                  'Two Pair' : 0,
                  'Three of a Kind' : 0,
                  'Straight' : 0,
                  'Flush' : 0,
                  'Full House' : 0,
                  'Four of a Kind' : 0,
                  'Straight Flush' : 0,
                  'Royal Flush' : 0}

    for _ in range(n):

        deck = treys.Deck()
        
        board = deck.draw(5) #ali pa vneses svoje --> treys.Card.new('Ah') --> ace of hearts
        hands_list = [#('player1', deck.draw(2)), #ali pa vneses svoje
                      #('player2', deck.draw(2)),
                      #('player3', deck.draw(2)),
                      #('player4', deck.draw(2)),
                      #('player5', deck.draw(2)),
                      ('player6', deck.draw(2))]

        eval = evaluate(hands_list, board)

        for element in hands_list:
            if element[0] == eval[0]:
                player_string = what_do_i_got(board, element[1])
                hands_dict[player_string] += 1

        #if len(eval) > 2:
            #print(eval)
            #print(treys.Card.print_pretty_cards(board))
            #for element in hands_list:
                #if element[0] in eval:
                    #print(treys.Card.print_pretty_cards(element[1]))
        if len(eval) == 1:
            results_dict[eval[0]] += 1
        else:
            for player in eval:
                results_dict[player] += 1
                results_dict['splits'] += 1

    for key in results_dict:    
        results_dict[key] /= n / 100
    for key in hands_dict:
        hands_dict[key] /= n / 100

    return results_dict, hands_dict
      

def combinations(n,k):
    all_posibilities = float(math.factorial(n) / (math.factorial(k) * math.factorial(n - k)))
    return all_posibilities

def calculate_probability(frequency):
    all_posibilities = combinations(52,5)
    return (frequency / all_posibilities) * 100

def poker_probabilities():

    royal_flush_frequency = combinations(4,1)
    royal_flush_probability = calculate_probability(royal_flush_frequency)

    straight_flush_frequency = combinations(4,1) * combinations(9,1)
    straight_flush_probability = calculate_probability(straight_flush_frequency)

    four_of_a_kind_frequency = combinations(13,1) * combinations(13-1,1) * combinations(4,1) # 13 cards, 12 possibilities for the fifth one and 4 colors
    four_of_a_kind_probability = calculate_probability(four_of_a_kind_frequency)

    full_house_frequency = combinations(13,1) * combinations(4,3) * combinations(13-1,1) * combinations(4,2) # first three: 13 cards, 4 posibilities, last two: 12 cards, 6 posibilities
    full_house_probability = calculate_probability(full_house_frequency)

    flush_frequency = (combinations(13,5) * combinations(4,1) - royal_flush_frequency - straight_flush_frequency)
    flush_probability = calculate_probability(flush_frequency)

    straight_frequency = combinations(10,1) * 4**5 - straight_flush_frequency # 10 possible sequences, 4 choices from all colours
    straight_probability = calculate_probability(straight_frequency)

    three_of_a_kind_frequency = combinations(13,1) * combinations(4,3) * combinations(13-1,2) * 4**2 # 13 cards, 4 posibilities, choose 2 from 12 cards,
    three_of_a_kind_probability = calculate_probability(three_of_a_kind_frequency)

    two_pair_frequency = combinations(13,2) * combinations(4,2)**2 * combinations(13-2,1) * combinations(4,1) # 2 pairs and the fifth card not from a pair
    two_pair_probability = calculate_probability(two_pair_frequency)

    one_pair_frequency = combinations(13,1) * combinations(4,2) * combinations(13-1,3)* combinations(4,1)**3 # 1 pair and three random cards without the one in the pair
    one_pair_probability = calculate_probability(one_pair_frequency)

    no_pair_frequency = (combinations(13,5) - 10) * (combinations(4,1)**5-4) # no pair
    no_pair_probability = calculate_probability(no_pair_frequency)

    return [no_pair_probability,
            one_pair_probability,
            two_pair_probability,
            three_of_a_kind_probability,
            straight_probability,
            flush_probability,
            full_house_probability,
            four_of_a_kind_probability,
            straight_flush_probability,
            royal_flush_probability]


probability_list = poker_probabilities()

start_time = time.time()
# main             
print(random_test(100000))
print(probability_list)
print("--- %s seconds ---" % (time.time() - start_time))