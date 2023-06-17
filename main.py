from __future__ import annotations
from enum import Enum, auto
#import os
from typing import Union
from dataclasses import dataclass
import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation, Window
from vi.config import Config
from serde.de import deserialize
from lib import Pray, Pred

WIDTH: int = 750
HEIGHT: int = 750

WINDOW: Window = Window(width=WIDTH, height=HEIGHT)

@dataclass
@deserialize
class Custom(Config):
    window: Window = WINDOW

custom = Custom()

test = Simulation(custom)

test.batch_spawn_agents(100, Pray, ["images/green.png"]).batch_spawn_agents(10, Pred, ["images/red.png"]).run()
