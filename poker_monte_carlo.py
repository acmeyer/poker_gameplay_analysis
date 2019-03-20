# -*- coding: utf-8 -*-
"""
Poker Monte Carlo.ipynb
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import itertools
from collections import defaultdict

# Seed
np.random.seed(0)

"""
# Simulation

## Gameplay  Functions
"""

# Functions to check winning hands
# modified from: https://briancaffey.github.io/2018/01/02/checking-poker-hands-with-python.html

def check_straight_flush(hand):
    if check_flush(hand):
        hand = get_flush(hand)
        if check_straight(hand) and len(hand) >= 5:
          return True
        else:
          return False
    else:
        return False

def check_four_of_a_kind(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values: 
        value_counts[v]+=1
    if 4 in sorted(value_counts.values()):
        return True
    return False

def get_quads(hand):
  values = [i[0] for i in hand]
  value_counts = defaultdict(lambda:0)
  for v in values: 
      value_counts[v]+=1
  return sorted([k for k,v in value_counts.items() if v==4], reverse=True)

def check_full_house(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values: 
        value_counts[v]+=1
    sorted_value_counts = sorted(value_counts.values())
    if 3 in sorted_value_counts:
      if sorted_value_counts.count(3) > 1:
        return True
      elif 2 in sorted_value_counts:
        return True
    return False
  
def get_full_house(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values: 
        value_counts[v]+=1
    sorted_value_counts = sorted(value_counts.values())
    return sorted([k for k,v in value_counts.items() if v==3 or v==2], reverse=True)

def check_flush(hand):
    suits = [i[1] for i in hand]
    suit_counts = defaultdict(lambda:0)
    for suit in suits: 
        suit_counts[suit]+=1
    if sorted(suit_counts.values(), reverse=True)[0] >= 5:
        return True
    else:
        return False

def get_flush(hand):
    suits = [i[1] for i in hand]
    suit_counts = defaultdict(lambda:0)
    for suit in suits: 
        suit_counts[suit]+=1
    top_suit_count = sorted(suit_counts.values(), reverse=True)[0]
    top_suit = sorted([k for k,v in suit_counts.items() if v==top_suit_count], reverse=True)[0]
    flush_cards = []
    for card in hand:
      if card[1] == top_suit:
        flush_cards.append(card)
    return flush_cards
      
def five_consecutive_cards(number_set):
  if len(number_set) < 5:
    return False
  
  for w, z in itertools.groupby(number_set, lambda x, y=itertools.count(): next(y)-x):
    grouped = list(z)
    if len(grouped) >= 5:
      return True
  return False

def get_highest_consecutive_card(number_set):
  for w, z in itertools.groupby(number_set, lambda x, y=itertools.count(): next(y)-x):
    grouped = list(z)
    if len(grouped) >= 5:
      return sorted(grouped, reverse=True)[0]

def check_straight(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values:
        value_counts[v] += 1

    set_of_values = set(values)    
    if five_consecutive_cards(set_of_values):
        return True
    else: 
        # Check straight with low Ace
        low_straight = set([14, 2, 3, 4, 5])
        if low_straight.issubset(set_of_values):
            return True
        return False
    
      
def get_straight_top_card(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values:
        value_counts[v] += 1

    set_of_values = set(values)    
    if five_consecutive_cards(set_of_values):
        return get_highest_consecutive_card(set_of_values)
    else: 
        # Straight with low Ace, 5 card is high
        return 5

def check_three_of_a_kind(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values: 
        value_counts[v]+=1
    if 3 in sorted(value_counts.values()):
        return True
    else:
        return False
      
def get_triples(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values: 
        value_counts[v]+=1
    return sorted([k for k,v in value_counts.items() if v==3], reverse=True)

def check_two_pairs(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values:
        value_counts[v]+=1
    if sorted(value_counts.values()).count(2) >= 2:
        return True
    else:
        return False

def check_one_pairs(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values:
        value_counts[v]+=1      
    if 2 in value_counts.values():
        return True
    else:
        return False
      
def get_pairs(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda:0)
    for v in values:
        value_counts[v]+=1
    return sorted([k for k,v in value_counts.items() if v == 2], reverse=True)
      
def check_hand(hand):
    if check_straight_flush(hand):
      return 9
    if check_four_of_a_kind(hand):
      return 8
    if check_full_house(hand):
      return 7
    if check_flush(hand):
      return 6
    if check_straight(hand):
      return 5
    if check_three_of_a_kind(hand):
      return 4
    if check_two_pairs(hand):
      return 3
    if check_one_pairs(hand):
      return 2
    return 1
  
def hand_type(hand):
  if check_straight_flush(hand):
    return 'straight flush'
  if check_four_of_a_kind(hand):
    return 'four of a kind'
  if check_full_house(hand):
    return 'full house'
  if check_flush(hand):
    return 'flush'
  if check_straight(hand):
    return 'straight'
  if check_three_of_a_kind(hand):
    return 'three of a kind'
  if check_two_pairs(hand):
    return 'two pairs'
  if check_one_pairs(hand):
    return 'one pair'

  return 'high card'
    
def get_high_cards(hand):
    values = [i[0] for i in hand]
    return sorted(values, reverse = True)
  
def compare_cards(first_hand, second_hand, num=None):
  first_high_cards = get_high_cards(first_hand)[:num]
  second_high_cards = get_high_cards(second_hand)[:num]
  
  for i in range(len(first_high_cards)):
    comparison = compare(first_high_cards[i], second_high_cards[i])
    if comparison != 0:
      return comparison
    
  return 0

def compare(card1, card2):
    if card1 > card2:
      return 1
    elif card1 < card2:
      return 2
    else:
      return 0

def break_tie(first_hand, second_hand):
    hand_score = check_hand(first_hand)
    
    if hand_score == 9:
      first_straight = get_straight_top_card(first_hand)
      second_straight = get_straight_top_card(second_hand)
      if first_straight > second_straight:
        return 1
      else:
        return 2
    if hand_score == 8:
      first_quads = get_quads(first_hand)[0]
      second_quads = get_quads(second_hand)[0]
      if first_quads > second_quads:
        return 1
      else:
        return 2
    if hand_score == 7:
      first_house = get_full_house(first_hand)[:2] # can only use 2
      second_house = get_full_house(second_hand)[:2] # can only use 2
      for i in range(len(first_house)):
        if first_house[i] > second_house[i]:
          return 1
        elif second_house[i] > first_house[i]:
          return 2
    if hand_score == 6:
      first_flush = get_flush(first_hand)
      second_flush = get_flush(second_hand)
      return compare_cards(first_flush, second_flush, 5)
    if hand_score == 5:
      first_straight = get_straight_top_card(first_hand)
      second_straight = get_straight_top_card(second_hand)
      if first_straight > second_straight:
        return 1
      elif second_straight > first_straight:
        return 2
      else:
        return 0
    if hand_score == 4:
      first_triples = get_triples(first_hand)[0]
      second_triples = get_triples(second_hand)[0]
      if first_triples > second_triples:
        return 1
      elif second_triples > first_triples:
        return 2
      else:
        # Drop triples
        first_hand = list(filter(lambda x: x[0] != first_triples, first_hand))
        second_hand = list(filter(lambda x: x[0] != second_triples, second_hand))           
        # Compare the rest
        return compare_cards(first_hand, second_hand, 2)
    if hand_score == 3:
      first_pairs = get_pairs(first_hand)
      second_pairs = get_pairs(second_hand)
      if first_pairs[0] > second_pairs[0]:
        return 1
      elif second_pairs[0] > first_pairs[0]:
        return 2
      elif first_pairs[1] > second_pairs[1]:
        return 1
      elif second_pairs[1] > first_pairs[1]:
        return 2
      else:
        # Drop pairs
        first_hand = list(filter(lambda x: x[0] not in first_pairs, first_hand))
        second_hand = list(filter(lambda x: x[0] not in second_pairs, second_hand))
        # Compare the rest
        return compare_cards(first_hand, second_hand, 1)
    if hand_score == 2:
      first_pair = get_pairs(first_hand)[0]
      second_pair = get_pairs(second_hand)[0]
      if first_pair > second_pair:
        return 1
      elif second_pair > first_pair:
        return 2
      else:
        # Drop pair
        first_hand = list(filter(lambda x: x[0] != first_pair, first_hand))
        second_hand = list(filter(lambda x: x[0] != second_pair, second_hand))
        # Compare the rest
        return compare_cards(first_hand, second_hand, 3)
    if hand_score == 1:
      return compare_cards(first_hand, second_hand)

    return 0

# Create a function to determine if player won, lost, or tied, given a series of hands and the cards on the board
def game_result(players_hand, other_players_hands, board):
  # Check other players hands value first
  best_other_player_hand = board + other_players_hands[0]
  for hand in other_players_hands:
    hand = hand + board
    if check_hand(hand) > check_hand(best_other_player_hand):
      best_other_player_hand = hand
    elif check_hand(hand) == check_hand(best_other_player_hand):
      is_tie = break_tie(hand, best_other_player_hand)
      if is_tie == 1:
        best_other_player_hand = hand 
 
  # Compare player's hand with best other player's hand
  players_hand = players_hand + board

  if check_hand(players_hand) > check_hand(best_other_player_hand):
    return 'Win'
  elif check_hand(players_hand) == check_hand(best_other_player_hand):
    is_tie = break_tie(players_hand, best_other_player_hand)
    if is_tie == 2:
      return 'Loss'
    elif is_tie == 1:
      return 'Win'
    else:
      return 'Tie'
    return 'Tie'
  else:
    return 'Loss'
  
  

# Create a function to determine what was the winning card combination, given a series of hands and the cards on the board
def winning_result(players_hands, board):
  best_player_hand = board + players_hands[0]
  for hand in players_hands:
    hand = hand + board
    if check_hand(hand) > check_hand(best_player_hand):
      best_player_hand = hand
    elif check_hand(hand) == check_hand(best_player_hand):
      is_tie = break_tie(hand, best_player_hand)
      if is_tie == 1:
        best_player_hand = hand 

  return hand_type(best_player_hand)

"""## Hold'em Function"""

# Create the deck of cards
# Deck key
# 11 = Jack, 12 = Queen, 13 = King, 14 = Ace
deck = list(itertools.product(range(2,15),['Spade','Heart','Diamond','Club']))

def holdem_simulation(players_hand, num_other_players, num_of_folding_players=0):
  # Copy deck for playing
  playing_deck = deck.copy()
  # Shuffle deck
  np.random.shuffle(playing_deck)

  # Remove players hand from playing deck
  playing_deck = list(filter(lambda x: x != players_hand[0], playing_deck))
  playing_deck = list(filter(lambda x: x != players_hand[1], playing_deck))

  # Create other players
  other_players_hands = []
  for i in range(num_other_players):
    other_players_hands.append([playing_deck.pop(0), playing_deck.pop(0)])

  # Game Play
  #========================
  # Simulate flop, turn, and river
  flop = playing_deck[0:4]
  del playing_deck[0:4] # remove from deck
  del flop[0] # burn card
  turn = playing_deck[0:2]
  del playing_deck[0:2] # remove from deck
  del turn[0] # burn card
  river = playing_deck[0:2]
  del playing_deck[0:2] # remove from deck
  del river[0] # burn card
  board = flop  + turn + river
  
  # Handle folding of other players if set
  if num_of_folding_players > 0 and num_of_folding_players < num_other_players:
    # Random folding
    folding_players = np.random.randint(1, num_other_players, num_of_folding_players)
    hands_to_delete = []
    for num in folding_players:
      hands_to_delete.append(other_players_hands[num])
    for hand in hands_to_delete:
      other_players_hands = list(filter(lambda x: x != hand, other_players_hands))
    
  
  return game_result(players_hand, other_players_hands, board)

second_deck = list(itertools.product(range(2,15),['Spade','Heart','Diamond','Club']))

def holdem_simulation_winning_hand(num_of_players):
  # Copy deck for playing
  second_playing_deck = second_deck.copy()
  # Shuffle deck
  np.random.shuffle(second_playing_deck)

  # Create players
  players_hands = []
  for i in range(num_of_players):
    players_hands.append([second_playing_deck.pop(0), second_playing_deck.pop(0)])

  # Game Play
  #========================
  # Simulate flop, turn, and river
  flop = second_playing_deck[0:4]
  del second_playing_deck[0:4] # remove from deck
  del flop[0] # burn card
  turn = second_playing_deck[0:2]
  del second_playing_deck[0:2] # remove from deck
  del turn[0] # burn card
  river = second_playing_deck[0:2]
  del second_playing_deck[0:2] # remove from deck
  del river[0] # burn card
  board = flop  + turn + river
  
  return winning_result(players_hands, board)

"""##  Game Simulation"""

# Game Simulation

def game(players_hand, num_of_other_players, game_sims, num_of_folding_players):
    wins = 0

    for i in range(game_sims):
      result = holdem_simulation(players_hand, num_of_other_players, num_of_folding_players)
      if result == 'Win' or result == 'Tie':
        wins += 1
        
    win_percentage = (wins / game_sims) * 100
    return win_percentage

# Functions to detect hand type
def is_pocket_pair(cards):
  if cards[0][0] == cards[1][0]:
    return True
  else:
    return False

def is_suited(cards):
  if cards[0][1] == cards[1][1]:
    return True
  else:
    return False
  
def is_connected(cards):
  if (cards[0][0] + 1) == cards[1][0]:
    return True
  elif (cards[0][0] - 1) == cards[1][0]:
    return True
  elif cards[0][0] == 14:
    if cards[1][0] == 2:
      return True
    else:
      return False
  elif cards[0][0] == 2:
    if cards[0][1] == 14:
      return True
    else:
      return False
  else:
    return False

# Functions to generate specific hand type
def get_suited_cards(suit, cards):
    potential_cards = list(filter(lambda x: x[1] == suit, cards))
    return potential_cards

def get_pair_cards(value, cards):
    potential_cards = list(filter(lambda x: x[0] == value, cards))
    return potential_cards

def get_connected_cards(value, cards):
    potential_cards = list(filter(lambda x: x[0] == value or x[0] == value + 1, cards))
    return potential_cards
  
def generate_hand(hand_type):
    deck = list(itertools.product(range(2,15),['Spade','Heart','Diamond','Club']))
    playing_deck = deck.copy()
    np.random.shuffle(playing_deck)
    players_hand = []

    if hand_type == 'suited':
      suits = ['Spade', 'Heart', 'Diamond', 'Club']
      np.random.shuffle(suits)
      suit = suits[0]
      players_hand = get_suited_cards(suit, playing_deck)[:2]
    elif hand_type == 'pairs':
      values = list(range(2,15))
      np.random.shuffle(values)
      value = values[0]
      players_hand = get_pair_cards(value, playing_deck)[:2]
    elif hand_type == 'connected':
      values = list(range(2,15))
      np.random.shuffle(values)
      value = values[0]
      connected_cards = get_connected_cards(value, playing_deck)
      first_card = connected_cards[0]
      potential_second_cards = list(filter(lambda x: x[0] != first_card[0], connected_cards))
      second_card = potential_second_cards[0]
      players_hand = [first_card, second_card]
    elif hand_type == 'connected_suited':
      suits = ['Spade', 'Heart', 'Diamond', 'Club']
      np.random.shuffle(suits)
      suit = suits[0]
      suited_cards = get_suited_cards(suit, playing_deck)
      values = list(range(2,15))
      np.random.shuffle(values)
      value = values[0]
      connected_cards = get_connected_cards(value, playing_deck)
      first_card = connected_cards[0]
      potential_second_cards = list(filter(lambda x: x[0] != first_card[0], connected_cards))
      second_card = potential_second_cards[0]
      players_hand = [first_card, second_card]
    else:
      return 'Unknown hand type!'

    return players_hand

"""## Analysis of Pocket Hands"""

hands_df = pd.DataFrame(columns=['Pocket Cards', 'Pair', 'Suited', 'Connected', 'Win Pct 8', 'Win Pct 7', 'Win Pct 6', 'Win Pct 5', 'Win Pct 4', 'Win Pct 3', 'Win Pct 2', 'Win Pct 1'])

# Go through every possible pocket cards combination
# and record winning % for games with varrying amount of players

# Setup
pocket_deck = list(itertools.product(range(2,15),['Spade','Heart','Diamond','Club']))
hand_combinations = list(itertools.combinations(pocket_deck, 2))
hand_combinations = [list(row) for row in hand_combinations]
num_of_folding_players = 0
game_sims = 10000
# Choose random hands
np.random.shuffle(hand_combinations)

# Simulate
for hand in hand_combinations:
  hand_dict = {'Pocket Cards': hand, 'Pair': is_pocket_pair(hand), 'Suited': is_suited(hand), 'Connected': is_connected(hand)}
  for i in range(1, 9):
    hand_dict['Win Pct ' + str(i)] = game(hand, i, game_sims, num_of_folding_players)
  hands_df = hands_df.append(hand_dict, ignore_index=True)

hands_df.head()

"""## What Wins"""

# Setup
wins_df = pd.DataFrame(columns=['Players Count', 'straight flush', 'four of a kind', 'full house', 'flush', 'straight', 'three of a kind', 'two pairs', 'one pair', 'high card'])
sims = 10000
hands_dict = {
  'straight flush': 0,
  'four of a kind': 0,
  'full house': 0,
  'flush': 0,
  'straight': 0,
  'three of a kind': 0,
  'two pairs': 0,
  'one pair': 0,
  'high card': 0
}

# Simulate
for n in range(2, 10):
  players_dict = {'Players Count': n, 'straight flush': 0, 'four of a kind': 0, 'full house': 0, 'flush': 0, 'straight': 0, 'three of a kind': 0, 'two pairs': 0, 'one pair': 0, 'high card': 0}
  for i in range(sims):
    result = holdem_simulation_winning_hand(n)
    players_dict[result] = players_dict[result] + 1

  wins_df = wins_df.append(players_dict, ignore_index=True)
  
wins_df = wins_df.rename(columns={'straight flush': 'Straight Flush Wins Pct', 'four of a kind': 'Four of a Kind Win Pct', 'full house': 'Full House Win Pct', 'flush': 'Flush Win Pct', 'straight': 'Straight Win Pct', 'three of a kind': 'Three of a Kind Win Pct', 'two pairs': 'Two Pairs Win Pct', 'one pair': 'One Pair Win Pct', 'high card': 'High Card Win Pct'})
column_names = ['Straight Flush Wins Pct', 'Four of a Kind Win Pct', 'Full House Win Pct', 'Flush Win Pct', 'Straight Win Pct', 'Three of a Kind Win Pct', 'Two Pairs Win Pct', 'One Pair Win Pct', 'High Card Win Pct']
wins_df[column_names] = wins_df[column_names].apply(lambda x: (x / sims) * 100)

wins_df

wins_df.to_csv('winning_poker_hands.csv')

"""## Pocket Card Frequency"""

new_deck = list(itertools.product(range(2,15),['C', 'D', 'H', 'S']))

def holdem_pocket_cards_simulation(num_of_players):
  # Copy deck for playing
  playing_deck = new_deck.copy()
  # Shuffle deck
  np.random.shuffle(playing_deck)

  # Create players
  players_hands = []
  for i in range(num_of_players):
    player_hand = [playing_deck.pop(0), playing_deck.pop(0)]
    player_hand.sort(key=lambda x: x[1])
    player_hand.sort(key=lambda x: x[0])
    player_hand = [str(row[0]) + '' + row[1] for row in player_hand]
    players_hands.append(player_hand)
    
  players_hands = [str(row[0]) + '/' + row[1] for row in players_hands]
  return players_hands

# Setup
game_sims = 10000

pocket_deck = list(itertools.product(range(2,15),['C', 'D', 'H', 'S']))
pocket_deck = [str(row[0]) + '' + row[1] for row in pocket_deck]
hand_combinations = list(itertools.combinations(pocket_deck, 2))
hand_combinations = [str(row[0]) + '/' + row[1] for row in hand_combinations]

hands_df = pd.DataFrame.from_dict({'Pocket Cards': hand_combinations})

# for each player count, simulate games
# for each game, record the pocket cards each player received
for n in range(2, 10):
  game_dict = {key:0 for key in hand_combinations}
  for i in range(game_sims):
    pocket_cards = holdem_pocket_cards_simulation(n)
    for result in pocket_cards:
      game_dict[result] += 1

  hands_df['Frequency w/ ' + str(n) + ' players'] = hands_df['Pocket Cards'].map(game_dict)

hands_df.tail(10)

def split_cards(hand):
  pocket = hand.split('/')
  card1 = pocket[0]
  card1 = (int(card1[:-1]), card1[-1])
  card2 = pocket[1]
  card2 = (int(card2[:-1]), card2[-1])
  
  return [card1, card2]

hands_df['Pocket Cards Tuple'] = hands_df['Pocket Cards'].apply(split_cards)

hands_df['Pair'] = hands_df['Pocket Cards Tuple'].apply(lambda x: is_pocket_pair(x))
hands_df['Suited'] = hands_df['Pocket Cards Tuple'].apply(lambda x: is_suited(x))
hands_df['Connected'] = hands_df['Pocket Cards Tuple'].apply(lambda x: is_connected(x))

hands_df = hands_df.drop(columns=['Pocket Cards Tuple'])

hands_df.tail()

hands_df.to_csv('pocket_cards_frequency.csv')