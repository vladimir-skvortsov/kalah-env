import os
import importlib
import json
from kalah import KalahGame
from test import get_move as student_agent

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

def main(agents_dir, games_num=20):
  agents = load_agents(agents_dir)
  grade = 0

  for agent_name, agent in agents.items():
    score = 0

    for _ in range(games_num // 2):
      game = KalahGame(student_agent, agent)
      result = game.play()

      if result == 0:
        score += 1
      elif result == 1:
        score -= 1

    for _ in range(games_num // 2):
      game = KalahGame(agent, student_agent)
      result = game.play()

      if result == 0:
        score -= 1
      elif result == 1:
        score += 1

    if score > 0:
      print(f'Student\'s agent won {agent_name}', score)
      grade += 1

  grade_dict = {'grade': grade}

  with open('grade.json', 'w') as json_file:
    json.dump(grade_dict, json_file)

if __name__ == '__main__':
  main('agents', games_num=20)
