def get_move(state):
  valid_moves = [i for i, house in enumerate(state) if house > 0 and 0 <= i <= 5]

  # Find the move that results in the most seeds in our own kalah
  most_seeds = -1
  best_moves = []
  for i in valid_moves:
    # Calculate the final position if we choose this move
    final_pos = (i + state[i]) % 13

    # Count the number of seeds in own kalah after the move
    seeds_in_kalah = state[6] + (1 if final_pos == 6 else 0)

    # Choose the move that results in the most seeds in our own kalah
    if seeds_in_kalah > most_seeds:
      most_seeds = seeds_in_kalah
      best_moves = [i]
    elif seeds_in_kalah == most_seeds:
      # If there are several equally good moves, store all of them
      best_moves.append(i)

  # If there are several moves that result in the maximum number of seeds,
  # choose the one that gives another move (lands in the own kalah) if possible
  for move in best_moves:
    final_pos = (move + state[move]) % 13
    if final_pos == 5:
      return move

  # If no such move exists, just return the first one of the best moves
  return best_moves[0]
