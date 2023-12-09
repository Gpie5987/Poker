from Range import Range
from PokerObject import Card
from Holdem import RangeExplorer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

utg_raiser = '44+,A2s+,K8s+,Q9s+,J9s+,T9s,98s,87s,76s,65s,ATo+,KJo+'
btn_raiser = '22+,A2s+,K2s+,Q2s+,J4s+,T6s+,96s+,85s+,74s+,63s+,53s+,43s,A2o+,K8o+,Q9o+,J8o+,T8o+,98o'
bbD_utg = 'JJ-22,AQs-A2s,K2s+,Q2s+,J7s+,T6s+,96s+,85s+,74s+,63s+,53s+,43s,AQo-ATo,KTo+,QTo+,JTo'
bbD_btn = '88-22,ATs-A6s,A3s-A2s,KTs-K2s,QJs,Q9s-Q2s,J7s-J2s,T7s-T2s,97s-93s,86s-83s,75s-73s,64s-63s,52s+,42s+,32s,AJo-A2o,K6o+,Q8o+,J8o+,T8o+,98o'


def create_js_file():
    board = 'Qh,Qd,3c'
    board_txt = board.split(',')
    range1 = Range(utg_raiser)
    range2 = Range(bbD_utg)
    board = []
    for card in board_txt:
        board.append(Card(card))
    range_explorer = RangeExplorer(range1,range2,board)
    range_explorer.create_js_file()
    
create_js_file()
