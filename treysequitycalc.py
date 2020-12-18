import treys
import random
import time

#INPUT TEST CASES

deck = treys.Deck().GetFullDeck()

roke = [[deck[0], deck[5]], [deck[1], deck[51]], [deck[45], deck[44]]]

#print(treys.Card.print_pretty_cards(roke[0]))
#print(treys.Card.print_pretty_cards(roke[1]))
#print(treys.Card.print_pretty_cards(roke[2]))

#flop = [deck[2], deck[25], deck[27]]
#flopturn = [deck[39], deck[43], deck[27], deck[12]]
#fullboard = [deck[6], deck[23], deck[8], deck[12], deck[34]]

#print(treys.Card.print_pretty_cards(flop))

evaluator = treys.Evaluator()

def equity_calculator(hands, board = None, n = 5000):
    '''vrne seznam seznamov - vsak podseznam vsebuje win % in tie %
       indeksi rezultatov sovpadajo z indeksi handov'''
    #tests
    if isinstance(hands, list):
        if len(hands) < 2 or len(hands) > 6:
            raise ValueError('Number of hands not correct!')
        for hand in hands:
            if not isinstance(hand, list):
                raise ValueError('Hand in hands should be list type!')
            for card in hand:
                if not isinstance(card, int):
                    raise ValueError('Card in hand is not integer type! '
                                     'Check if deck.GetFullDeck()!')
    else:
        raise ValueError('Hands parameter should be list type!')

    if board:
        if isinstance(board, list):
            if (len(board) == 1 or len(board) == 2 or len(board) > 5):
                raise ValueError('Board length not correct!')
            for card in board:
                if not isinstance(card, int):
                    raise ValueError('Card in board is not integer type! '
                                     'Check if deck.GetFullDeck()!')
        else:
            raise ValueError('Board should be list type!')

        for hand in hands:
            for card in hand:
                if card in board:
                    raise TypeError('Incorrect input! '
                                    'Matching cards in hands and board!')
    
    
    final_list = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    
    #ce je full board, pogledamo samo enkrat kdo je zmagovalec

    if board and len(board) == 5:
        winners_list = []
        for hand in hands:
            winners_list.append(evaluator.evaluate(board, hand))
        najboljsi = min(winners_list)
        sez = [i for i, x in enumerate(winners_list) if x == najboljsi]
        if len(sez) == 1:
            final_list[sez[0]][0] += 100.0
        else:
            for index in sez:
                final_list[index][1] += 100.0
    else:
        for _ in range(n):
            #za vsako nov dek, jebiga
            deck = treys.Deck().GetFullDeck()
            #vzamem iz deka karte od igralcev
            for hand in hands:
                for card in hand:
                    deck.pop(deck.index(card))
            #zmesam
            random.shuffle(deck)
            #ce je board none, govorimo o preflop eq. Board treba naredit
            if board == None:
                board = deck[:5]
                #zapenjam score v winner list
                winners_list = []
                for hand in hands:
                    winners_list.append(evaluator.evaluate(board, hand))
                #board nastavis nazaj na none
                board = None
                najboljsi = min(winners_list)
                #sez je seznam indeksov zmagovalnih kart (lahko enih ali vecih)
                sez = [i for i, x in enumerate(winners_list) if x == najboljsi]
                #če je sam en, ni split
                if len(sez) == 1:
                    final_list[sez[0]][0] += 1 #štej zmago
                else: #mamo split
                    for index in sez:
                        final_list[index][1] += 1 #štej split
            #ce so 3 na boardu, govorimo o postflop eq
            elif len(board) == 3:
                #vrzem iz deka karte iz boarda!
                for card in board:
                    deck.pop(deck.index(card))
                #dodam turn in flop
                board.append(deck[0])
                board.append(deck[1])
                winners_list = []
                for hand in hands:
                    winners_list.append(evaluator.evaluate(board, hand))
                #board nastavis nazaj
                board.remove(deck[0])
                board.remove(deck[1])
                najboljsi = min(winners_list)
                sez = [i for i, x in enumerate(winners_list) if x == najboljsi]
                if len(sez) == 1:
                    final_list[sez[0]][0] += 1
                else:
                    for index in sez:
                        final_list[index][1] += 1
            #ce so 4 na boardu govorimo o postturn eq
            elif len(board) == 4:
                for card in board:
                    deck.pop(deck.index(card))
                #dodam river
                board.append(deck[0])
                winners_list = []
                for hand in hands:
                    winners_list.append(evaluator.evaluate(board, hand))
                #board nastavis nazaj
                board.remove(deck[0])
                najboljsi = min(winners_list)
                sez = [i for i, x in enumerate(winners_list) if x == najboljsi]
                if len(sez) == 1:
                    final_list[sez[0]][0] += 1
                else:
                    for index in sez:
                        final_list[index][1] += 1
        #se zdelim rezultate
        for score in final_list:
            score[0] /= n / 100
            score[1] /= n / 100

    return final_list


start_time = time.time()
print(equity_calculator(roke))
print('Completed in ' + str(time.time() - start_time) + ' seconds.')