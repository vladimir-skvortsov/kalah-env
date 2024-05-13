import os
from importlib.util import spec_from_file_location, module_from_spec
import json
from kalah import KalahGame
from task import get_move as student_agent

def load_agents(agents_dir):
  agents = {}

  for agent_file in os.listdir(agents_dir):
    if agent_file.endswith('.py'):
      name = agent_file[:-3]
      abs_path = os.path.join(agents_dir, agent_file)
      spec = spec_from_file_location(name, abs_path)
      module = module_from_spec(spec)
      spec.loader.exec_module(module)
      agents[name] = module.get_move

  return agents

def save_grade(grade):
  grade_dict = {'grade': grade}
  with open('grade.json', 'w') as json_file:
    json.dump(grade_dict, json_file)

def main(agents_dir, games_num=20):
  agents = load_agents(agents_dir)
  grade = 0

  for agent_name, agent in agents.items():
    score = 0

    try:
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
    except Exception as exception:
      save_grade(str(exception))
      return

    if score > 0:
      print(f'Student\'s agent won {agent_name} with score {score}')
      grade += 1
    elif score == 0:
      print(f'Student\'s agent played in a draw with {agent_name}')
      grade += 0.5
    else:
      print(f'Student\'s agent lost {agent_name} with score {score}')

  save_grade(int(grade))

if __name__ == '__main__':
  main('agents', games_num=20)
