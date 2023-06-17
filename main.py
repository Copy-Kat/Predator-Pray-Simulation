from __future__ import annotations
from enum import Enum, auto
#import os
from typing import Union
from dataclasses import dataclass
import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation, Window
from vi.config import Config

from lib import Pray, Pred, PPConfig



custom = PPConfig()

test = Simulation(custom)

test.batch_spawn_agents(1, Pray, ["images/green.png"]).batch_spawn_agents(20, Pred, ["images/red.png"]).run()
