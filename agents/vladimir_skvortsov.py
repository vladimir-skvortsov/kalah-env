import random

def get_move(state):
  valid_moves = [i for i, house in enumerate(state) if house > 0 and 0 <= i <= 5]
  return random.choice(valid_moves)

if __name__ == '__main__':
  game_state = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
  print(get_move(game_state))

