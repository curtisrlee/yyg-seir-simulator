import subprocess
import os

print(os.getcwd())

cmd = """run_simulation.py -v --best_params_dir best_params/latest --country US -g \
--simulation_end_date 2021-05-30 \
--set_param REOPEN_R 1.22 \
--set_param REOPEN_INFLECTION 0.22 \
--set_param POST_REOPEN_EQUILIBRIUM_R .87 \
--set_param FALL_R_MULTIPLIER 1.025"""

simulations = [
  {},
  {
    'VAX_PEAK_RATIO_PER_DAY': 0.0
  },
  {
    'VAX_ACCESS': 0.5
  },
  {
    'VAX_ACCESS': 1.5
  },
]

for simulation in simulations:
  extra = []
  for key, value in simulation.items():
    extra.append('--set_param')
    extra.append(str(key))
    extra.append(str(value))

  result = subprocess.check_output(['python', *cmd.split(), *extra])
  for line in result.splitlines()[-7:-2]: 
    line = line.decode()
    # print(line) 
    data = line.split(':')
    key = data[0].strip()
    value = data[1].strip()
    print(key, value)
  