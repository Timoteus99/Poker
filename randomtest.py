import matplotlib.pyplot as plt
import treys
import time
import math
import os

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

def run_tests(n):

    probabilities = poker_probabilities()
    evaluator = treys.Evaluator()

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
    abs_diff = []
    for _ in range(n):
        deck = treys.Deck()
        player = deck.draw(2)
        board = deck.draw(3)
        player_score = evaluator.evaluate(board, player)
        player_string = evaluator.get_rank_class(player_score)
        final_string = evaluator.class_to_string(player_string)
        hands_dict[final_string] += 1
    i = 0
    for key in hands_dict:
        hands_dict[key] /= n / 100
        abs_diff.append(abs(hands_dict[key] - probabilities[i]))
        i += 1
    return [hands_dict, abs_diff]

def write_tests(file_name, n):
    tests = run_tests(n)
    probabilities = poker_probabilities()
    f = open(file_name, "r") #zamenjaj z 'w' ce hoces prepisat, ali 'a' za append
    f.write('Testing TREYS random\n')
    f.write('Dealt ' + str(n) + ' times\n')
    f.write('Flush calc example eq: times_flush_fallen / all_games\n')
    i = 0
    for key in tests[0].keys():
        f.write('Probability of getting ' + key + ' is: ' + str(round(probabilities[i], 6)) + '%, we got: ' + str(tests[0][key]) + '%' + ', absolute difference is: ' + str(tests[1][i]) + '\n')
        i += 1
    f.close()

#start_time = time.time()
#i = 10
#while i <= 1000000:
   #write_tests("randomtest.txt", i)
   #i *= 10
#print(str(time.time() - start_time) + ' seconds')

def read_draw(file_name):
    absolute_differences = []
    average_differences = []
    tries = [1, 10, 100, 1000, 10000, 100000, 1000000]
    f = open(file_name, "r")
    line_list = f.readlines()
    f.close()
    for line in line_list:
        try:
            float(line.split(':')[-1])
            absolute_differences.append(float(line.split(':')[-1].rstrip()))
        except:
            pass
    i = 0
    j = 10
    while i <= 60:
        average_differences.append(sum(absolute_differences[i:j]) / 10)
        i += 10
        j += 10

    plt.plot(tries, average_differences, 'r--')
    plt.yscale('symlog', linthreshy = 0.1)
    plt.xscale('symlog', linthreshy = 0.1)
    plt.title('TREYS random test')
    plt.xlabel('Number of games')
    plt.ylabel('Absolute difference between real and calculated in %')
    plt.grid()
    plt.savefig('testsgraph.png')

    return plt.show(), average_differences

#print(read_draw("randomtest.txt"))