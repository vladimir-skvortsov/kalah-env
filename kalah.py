from state import State

class KalahGame:
  def __init__(self, agent1, agent2):
    self.agents = [agent1, agent2]

  def reset(self, current_player=0):
    self.turn = 1
    self.board = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
    self.current_player = current_player

  def switch_player(self):
    self.current_player = 1 - self.current_player

  def get_opposite_house(self, index):
    return 12 - index

  def get_opponents_kalah(self):
    return 13 if self.current_player == 0 else 6

  def move_seeds(self, house):
    seeds = self.board[house]
    opponents_kalah = self.get_opponents_kalah()

    self.board[house] = 0

    index = house

    while seeds > 0:
      index = (index + 1) % 14

      # Skip opponent's kalah
      if index != opponents_kalah:
        self.board[index] += 1
        seeds -= 1

    return index

  def get_valid_moves(self):
    start = self.current_player * 6
    end = (self.current_player + 1) * 6
    return [i for i in range(start, end) if self.board[i] > 0]

  def play(self, current_player=0):
    self.reset(current_player)

    while max(self.board[0:6]) > 0 and max(self.board[7:13]) > 0:
      agent = self.agents[self.current_player]
      valid_moves = self.get_valid_moves()

      try:
        chosen_move = agent(list(self.board))
      except Exception as e:
        print(e)
        return 1 - self.current_player

      if not chosen_move in valid_moves:
        return 1 - self.current_player

      last_seed_index = self.move_seeds(chosen_move)

      # Extra turn
      if last_seed_index == 6 or last_seed_index == 13:
        self.turn += 1
        continue

      # Capture
      if self.board[last_seed_index] == 1 and last_seed_index >= self.current_player * 6 and last_seed_index < (self.current_player + 1) * 6:
        opposite_house = self.get_opposite_house(last_seed_index)
        self.board[6 + self.current_player * 7] += 1 + self.board[opposite_house]
        self.board[last_seed_index] = 0
        self.board[opposite_house] = 0

      self.turn += 1
      self.switch_player()

    return 1 if self.board[6] > self.board[13] else (-1 if self.board[6] < self.board[13] else 0)







