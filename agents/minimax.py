import copy

def is_game_over(state):
  return sum(state[0:6]) == 0 or sum(state[7:13]) == 0

def evaluate_state(state):
  return state[6] - state[13]

def minimax(state, depth, maximize=True):
  if depth == 0 or is_game_over(state):
    return evaluate_state(state), None

  best_score = -float('inf') if maximize else float('inf')
  best_move = None
  for i in range(6):
    if state[i] == 0:
      continue

    new_state = copy.deepcopy(state)
    # Execute the move
    new_state[i] = 0
    score, _ = minimax(new_state, depth-1, not maximize)

    if maximize and score > best_score:
      best_score, best_move = score, i
    elif not maximize and score < best_score:
      best_score, best_move = score, i

  return best_score, best_move

def get_move(state):
  _, move = minimax(state, 8)
  return move
