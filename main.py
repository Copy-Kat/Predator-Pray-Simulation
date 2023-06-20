import os

from lib import Grass, PPConfig, PPSim, Pray, Pred

config = PPConfig()

assert (
    len(config.grass_location) == config.grass_count
), "Number of grass location not matched with the number location passed. Check GRASS_COUNT or grass_location for error"

test = PPSim(config)

df = (
    test.batch_spawn_agents(config.pray_count, Pray, ["images/green.png"])
    .batch_spawn_agents(config.pred_count, Pred, ["images/red.png"])
    .batch_spawn_agents(config.grass_count, Grass, ["images/white.png"])
    .run()
    .snapshots
)

file_name = "data.csv"

print(df)

if not os.path.exists(file_name):
    with open(file_name, "w"):
        pass

df.write_csv(file_name, separator=",")

print("Output: ", file_name)
