def get_move(state):
  max_value = max(state[0:6])
  return state.index(max_value)
