def evaluate_next_states(state):
  scores = []

  for i in range(6):
    seeds = state[i]

    # Check for empty pit
    if seeds == 0:
      scores.append(0)
      continue

    expected_position = (i + seeds) % 14
    if expected_position < 6:
      scores.append(seeds)
    elif expected_position == 6:
      scores.append(seeds + 1)
    else:
      scores.append(seeds - 1)

  return scores

def get_move(state):
  scores = evaluate_next_states(state)
  max_value = max(scores)
  return scores.index(max_value)
