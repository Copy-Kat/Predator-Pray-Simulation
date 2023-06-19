from dataclasses import dataclass
from serde.de import deserialize
from vi import Agent, Simulation, Window, Config
import random
from typing import Optional
import pygame as pg


WIDTH: int = 750
HEIGHT: int = 750
COLLIDE_DISTANCE: int = 8 # distance between 2 agents to count as collided
BG_COLOR: tuple[int, int, int] = (50, 50, 50) # chance bg_color if needed

WINDOW: Window = Window(width=WIDTH, height=HEIGHT)

@dataclass
@deserialize
class QOLConfig(Config):
    visualise_chunks: bool = True
    print_fps: bool = False

@dataclass
@deserialize
class PPConfig(QOLConfig):
    window: Window = WINDOW
    change_dir_chance: float = 0.25 # can change if needed
    radius: int = 50 # maybe improvement here?

    pray_base_chance_reproduce: float = 0.25 # need polish
    pray_reproduce_pulse_timer: int = 100 # need polish

    pred_base_chance_dying: float = 0.1 # need polish
    pred_death_pulse_timer: int = 100 # need polish

# Pray class
class Pray(Agent):
    config: PPConfig
    reproduce_timer: int = 100 # time between each reproduce attempt

    def update(self):
        self.save_data("kind", "Pray") # save data for later
        
        if self.reproduce_timer == 0:

            p = random.random()

            # reproduce
            if self.config.pray_base_chance_reproduce > p:
                self.reproduce()

                self.move.rotate_ip(90)
            
            # reset timer regardless
            self.reproduce_timer = self.config.pray_reproduce_pulse_timer
            return
            
        self.reproduce_timer -= 1 

    
    def change_position(self): # basic random move

        self.there_is_no_escape()

        prng = self.shared.prng_move

        should_change_dir = prng.random()

        if self.config.change_dir_chance > should_change_dir:
                self.move.rotate(prng.uniform(-10, 10))

        self.pos += self.move

# Pred class
class Pred(Agent):
    config: PPConfig
    target: Pray
    death_timer: int
    hunger: int = 100
    dying: bool = False

    def update(self):

        self.save_data("kind", "Pred") # save data
        
        # if no more hunger then enter dying state
        if self.hunger == 0 and not self.dying: 
            self.death_timer = self.config.pred_death_pulse_timer
            self.dying = True
        
        # count down the timer till death door
        if self.dying:
            if self.death_timer == 0:

                p = random.random()

                if p < self.config.pred_base_chance_dying:
                    self.kill()
                return

            self.death_timer -= 1

        self.hunger -= 1
        

    def change_position(self):

        self.there_is_no_escape()
        
        # aquire target
        targets = list(self.in_proximity_accuracy().filter_kind(Pray))

        if targets: # if target found
        
            targets = sorted(targets, key = lambda x : x[1]) # sort targets

            self.target = targets[0][0] # get closest target
        
            if (self.target.pos - self.pos).length() < COLLIDE_DISTANCE:
                self.target.kill() # kill if collided
                self.hunger = 100
                if self.dying:
                    self.dying = False
                self.pos += self.move
                return

            self.move = (self.target.pos - self.pos)

        else: # random walk
        
            prng = self.shared.prng_move

            should_change_dir = prng.random()

            if self.config.change_dir_chance > should_change_dir:
                    self.move.rotate(prng.uniform(-10, 10))
        
        self.pos += self.move.normalize() * 1.5 # make pred faster than prey

class PPSim(Simulation):
    def __init__(self, config: Optional[Config] = None):
        super().__init__(config)

        pg.display.init()
        pg.display.set_caption("Violet")

        size = self.config.window.as_tuple()
        self._screen = pg.display.set_mode(size)

        # Initialise background
        self._background = pg.surface.Surface(size).convert()
        self._background.fill(BG_COLOR)

        # Show background immediately (before spawning agents)
        self._screen.blit(self._background, (0, 0))
        pg.display.flip()

        # Initialise the clock. Used to cap FPS.
        self._clock = pg.time.Clock()
