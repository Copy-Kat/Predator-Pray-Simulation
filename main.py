from __future__ import annotations
from enum import Enum, auto
import os
from typing import Union
from dataclasses import dataclass
import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation, Window
from vi.config import Config

from lib import Pray, Pred, PPConfig



custom = PPConfig()

test = Simulation(custom)

df = test.batch_spawn_agents(100, Pray, ["images/green.png"]).batch_spawn_agents(30, Pred, ["images/red.png"]).run().snapshots

file_name = "data.csv"

print(df)

if not os.path.exists(file_name):
    with open(file_name, 'w'): pass

df.write_csv(file_name, separator=",")

print("Output: ", file_name)
