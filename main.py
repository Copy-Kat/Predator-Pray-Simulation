import os

from lib import Pray, Pred, PPConfig, PPSim

custom = PPConfig()

test = PPSim(custom)

df = test.batch_spawn_agents(100, Pray, ["images/green.png"]).batch_spawn_agents(30, Pred, ["images/red.png"]).run().snapshots

file_name = "data.csv"

print(df)

if not os.path.exists(file_name):
    with open(file_name, 'w'): pass

df.write_csv(file_name, separator=",")

print("Output: ", file_name)
