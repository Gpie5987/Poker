
#測試EquityExplorer
from Holdem import EquityExplorer
from Range import Range
from Holdem import Holdem
from PokerObject import Deck
from PokerObject import Card
from PokerObject import Hand
from PokerHand import PokerHand
import time
import random

#EquityExplorer.range_battle()誤差測試
def range_battle():
    ip_range = Range('44+,A2s+,K2s+,Q4s+,J6s+,T7s+,97s+,87s,A2o+,K6o+,Q8o+,J8o+,T8o+')
    oop_range = Range('7s7c')
    ip_win = 0
    oop_win = 0
    draw = 0
    for ip_hand in ip_range.hands:
        for oop_hand in oop_range.hands:
            i += 1
            deck = Deck()
            deck.remove_cards(ip_hand.cards+oop_hand.cards)
            draw_5 = deck.draw(5)
            rst = Holdem.compare_two_hand(ip_hand,oop_hand,draw_5)
            if rst == ip_hand:
                ip_win += 1
            elif rst == oop_hand:
                oop_win += 1
            else:
                draw += 1
    return (ip_win+draw/2)/(ip_win+oop_win+draw)
def error_test():
    error = []
    for i in range(15):
        rst = range_battle()
        print(i,':',rst)
        error.append(abs(rst - 0.4401))
    print('average error:',sum(error)/len(error))
    print('max error:',max(error))
#EquityExplorer.get_results測試
def get_results_test():
    ip_range = Range('44+,A2s+,K2s+,Q4s+,J6s+,T7s+,97s+,87s,A2o+,K6o+,Q8o+,J8o+,T8o+')
    oop_range = Range('77')
    board = [Card('2d'),Card('Qh'),Card('Tc')]
    match1 = EquityExplorer(ip_range,oop_range,board)
    ip_results,oop_results = match1.get_results()
    for i in range(10):
        print(ip_results[i])
    print('ip_len:',len(ip_results))
    print('==================================')
    print('oop_len:',len(oop_results))
    for i in range(6):
        print(oop_results[i])

#測試RangeExplorer
from Holdem import RangeExplorer
def sort_ranking_test():
    rang = Range('AJo-A2o,99+')
    re = RangeExplorer(rang,rang,[Card('8s'),Card('2s'),Card('7s')])
    poker_hands = RangeExplorer.range_to_MyPH_combo(re.IP_range,re.board,'IP')
    ph_rank = RangeExplorer.sort_ranking(poker_hands)
    PokerHand_PR = RangeExplorer.make_PR_distribution(ph_rank)

    for i,PR in enumerate(PokerHand_PR):
        print(i+1,':',end='')
        for my_PH in PR:
            print(my_PH.hand,end=' ')
        print()
    print('len:',len(PokerHand_PR))
'''------------------exe---------------------------'''
#測試_output_PR
def output_PR_test():
    range1 = Range('AJo-A2o,99+')
    range2 = Range('KJs-K2s')
    board = [Card('8s'),Card('2s'),Card('7s')]
    range_explorer = RangeExplorer(range1,range2,board)
    r1,r2 = range_explorer.get_PR()
    r1_ouput,r2_output = range_explorer.create_js_file()
    for i,r1 in enumerate(r1_ouput):
        print(i,':',end=' ')
        if r1 != None:
            for r in r1:
                print(r.hand,end=',')
        else:
            print(r1,end='')
        print()
    print('----------------')
    for i,r1 in enumerate(r2_output):
        print(i,':',end=' ')
        if r1 != None:
            for r in r1:
                print(r.hand,end=',')
        else:
            print(r1,end='')
        print()
# _build_output_txt測試
def build_output_txt_test():
    range1 = Range('AJo-A2o,99+')
    range2 = Range('KJs-K2s')
    board = [Card('8s'),Card('2s'),Card('7s')]
    range_explorer = RangeExplorer(range1,range2,board)
    r1_ouput,r2_output = range_explorer.create_js_file()
    print(r1_ouput)
    print(r2_output)
#測試create_js_file
def create_js_file_test():
    range1 = Range('AJo-A2o,99+')
    range2 = Range('KJs-K2s')
    board = [Card('8s'),Card('2s'),Card('7s')]
    range_explorer = RangeExplorer(range1,range2,board)
    range_explorer.create_js_file()

#測試_get_card_distribution和_create_ph_type_dict
def _get_card_distribution_test():
    range1 = Range('AJo-A2o,99+')
    board = [Card('8s'),Card('2s'),Card('7s')]
    poker_hands = RangeExplorer.range_to_MyPH_combo(range1,board)
    rst = RangeExplorer.get_card_distribution(poker_hands)
    print(rst)
start_time = time.time()

_get_card_distribution_test()
end_time = time.time()
print('time:',end_time-start_time)
print('END')

