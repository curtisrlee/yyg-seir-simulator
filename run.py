import subprocess
import os
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import time

print(os.getcwd())

cmd = """run_simulation.py -v --best_params_dir best_params/latest --country US -g \
--simulation_end_date 2021-05-30 \
--set_param REOPEN_R 1.22 \
--set_param REOPEN_INFLECTION 0.22 \
--set_param POST_REOPEN_EQUILIBRIUM_R .87 \
--set_param FALL_R_MULTIPLIER 1.025"""

simulations = [
  {
    'VAX_ACCESS': 1.0
  },
  {
    'VAX_ACCESS': 1.5
  },
  {
    'VAX_ACCESS': 0
  },
  {
    'VAX_ACCESS': 0.5
  },
  {
    'VAX_ACCESS': 1.0,
    'VAX_START_DATE': '2021-1-11'
  },
  {
    'VAX_ACCESS': 0.5,
    'VAX_START_DATE': '2021-1-11'
  },
  {
    'VAX_SIGMA': 0.2,
  },
  {
    'VAX_SIGMA': 0.05,
  },
  {
    'VAX_ACCESS': 0.35,
    'VAX_SIGMA': 93
  },
]

results = []

for simulation in simulations:
  result = {}
  extra = []
  for key, value in simulation.items():
    extra.append('--set_param')
    extra.append(str(key))
    extra.append(str(value))
    result[key] = value
    
  output = subprocess.check_output(['python', *cmd.split(), *extra])
  output_lines = output.splitlines()
  for line in output_lines[-7:-2]: 
    line = line.decode()
    # print(line) 
    data = line.split(':')
    key = data[0].strip()
    value = data[1].strip()
    # print(key, value)
    result[key] = value
  
  results.append(result)
  time.sleep(1)

df = pd.DataFrame(results)
# df = df.astype({'VAX_PEAK_RATIO_PER_DAY': bool})
df = df.rename(columns={'VAX_ACCESS': 'Vaccination Ratio'})
df = df.drop(columns=['End of simulation', 'Peak hospital beds used', 'VAX_START_DATE'])
df.to_csv('plot/results.csv')

print(df)

# print(results)