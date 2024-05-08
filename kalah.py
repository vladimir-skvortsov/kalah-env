class KalahGame:
  def __init__(self, agent1, agent2):
    self.agents = [agent1, agent2]
    self.board = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
    self.current_player = 0

  def switch_player(self):
    self.current_player = 1 - self.current_player

  def get_opposite_house(self, index):
    return 12 - index

  def get_opponents_kalah_index(self):
    return 13 if self.current_player == 0 else 6

  def move_seeds(self, house):
    seeds = self.board[house]
    opponents_kalah = self.get_opponents_kalah_index()

    self.board[house] = 0

    index = house

    while seeds > 0:
      index = (index + 1) % 14

      # Skip opponent's kalah
      if index != opponents_kalah:
        self.board[index] += 1
        seeds -= 1

    return index

  def get_agent_board_representation(self):
    if self.current_player == 0:
      return list(self.board)
    return self.board[7:] + self.board[0:7]

  def get_valid_moves(self):
    board = self.get_agent_board_representation()
    return [i for i in range(0, 6) if board[i] > 0]

  def get_chosen_move_representation(self, chosen_move):
    if self.current_player == 0:
      return chosen_move
    return 7 + chosen_move


  def play(self):
    while max(self.board[0:6]) > 0 and max(self.board[7:13]) > 0:
      agent = self.agents[self.current_player]
      valid_moves = self.get_valid_moves()

      board = self.get_agent_board_representation()

      try:
        chosen_move = agent(board)
      except Exception as e:
        print(e)
        return 1 - self.current_player

      if not chosen_move in valid_moves:
        print('chosen_move', chosen_move)
        return 1 - self.current_player

      chosen_move = self.get_chosen_move_representation(chosen_move)
      last_seed_index = self.move_seeds(chosen_move)

      # Extra turn
      if last_seed_index == 6 or last_seed_index == 13:
        continue

      # Capture
      if self.board[last_seed_index] == 1 and last_seed_index >= self.current_player * 6 and last_seed_index < (self.current_player + 1) * 6:
        opposite_house = self.get_opposite_house(last_seed_index)
        self.board[6 + self.current_player * 7] += 1 + self.board[opposite_house]
        self.board[last_seed_index] = 0
        self.board[opposite_house] = 0

      self.switch_player()

    # agent1 won
    if self.board[6] > self.board[13]:
      return 0
    # agent2 won
    if self.board[6] < self.board[13]:
      return 1
    # draw
    return 0.5
