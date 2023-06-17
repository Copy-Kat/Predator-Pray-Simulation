from enum import Enum, auto
#import os
from typing import Union

# use numpy for another rng genrator
# doc said movement use a decoupled rng
# use random.random may affect the rng of movement
# haven't tested the theory but add here just in case
#import numpy as np
from pygame.gfxdraw import hline, vline

import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation
from vi.config import Config, dataclass, deserialize
