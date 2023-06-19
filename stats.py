import polars as pl
import os

df = pl.read_csv("data.csv")

df.groupby(["frame", "kind"], maintain_order=True).count()

clean = df.groupby("frame", maintain_order=True).agg([
    pl.col("kind").filter(pl.col("kind") == "Pred").count().alias("Pred count"),
    pl.col("kind").filter(pl.col("kind") == "Pray").count().alias("Pray count")
    ])

file_name = "Population.csv"

if not os.path.exists(file_name):
    with open(file_name, 'w'): pass

clean.write_csv(file_name, separator=",")

print(clean)
