import os
import importlib
import pandas as pd
from collections import defaultdict
from itertools import combinations

# Assuming your game module is named `kalah`
from kalah import KalahGame

def load_agents(agents_dir):
  agents = {}

  for agent_file in os.listdir(agents_dir):
    if agent_file.endswith('.py'):
      name = agent_file[:-3]
      abs_path = os.path.join(agents_dir, agent_file)
      spec = importlib.util.spec_from_file_location(name, abs_path)
      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)
      agents[name] = module.get_move

  return agents

def calculate_sonneborn_berger(scores_df):
  sonneborn_berger_scores = {}

  for bot in scores_df.columns:
    sonneborn_berger_scores[bot] = sum(opponent_score * score for opponent_score, score in zip(scores_df.sum(), scores_df.loc[bot]))

  return sonneborn_berger_scores

def main(agents_dir):
  agents = load_agents(agents_dir)
  scores_df = pd.DataFrame(index=agents.keys(), columns=agents.keys())
  scores_df = scores_df.infer_objects(copy=False).fillna(0)

  for pair1, pair2 in combinations(agents.items(), 2):
    agent_name1, agent1 = pair1
    agent_name2, agent2 = pair2

    sum_score = 0

    for game_index in range(10):
      game = KalahGame(agent1, agent2)
      result = game.play(current_player=game_index % 2)

      if result == 0:
        sum_score += 1
      elif result == 1:
        sum_score -= 1

    if sum_score > 0:
      score = 1
    elif sum_score < 0:
      score = 0
    else:
      score = 0.5

    print(agent_name1, agent_name2, sum_score, score),

    scores_df.loc[agent_name1, agent_name2] = score
    scores_df.loc[agent_name2, agent_name1] = 1 - score

  sonneborn_berger_scores = calculate_sonneborn_berger(scores_df)

  print(scores_df)
  scores_df.to_csv('bot_scores.csv')
  with open('sonneborn_berger.txt', 'w') as f:
    for bot_name, sb_score in sonneborn_berger_scores.items():
      f.write(f"{bot_name}: {sb_score}\n")

if __name__ == '__main__':
  main('agents')
