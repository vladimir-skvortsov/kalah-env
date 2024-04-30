import random

def get_move(state):
  valid_moves = [i for i, house in enumerate(state) if house > 0 and 0 <= i <= 5]
  return valid_moves[-1]
