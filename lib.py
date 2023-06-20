from dataclasses import dataclass, field
from pygame.color import Color
from pygame.math import Vector2
from serde.de import deserialize
from vi import Agent, Simulation, Window, Config
import random
from typing import Optional
import pygame as pg
from pygame.gfxdraw import hline, vline

pg.init()

WIDTH: int = 750
HEIGHT: int = 750
COLLIDE_DISTANCE: int = 8 # distance between 2 agents to count as collided
BG_COLOR: tuple[int, int, int] = (0, 0, 0) # chance bg_color if needed
TEXT_COLOR: tuple[int, int, int] = (255, 255, 255)

grass_color: Color =  Color(120, 135, 100, 90)

WINDOW: Window = Window(width=WIDTH, height=HEIGHT)

FONT_SIZE: int = 20
FONT = pg.font.SysFont("Arial", FONT_SIZE)


@dataclass
@deserialize
class QOLConfig(Config):
    visualise_chunks: bool = True
    print_fps: bool = True
    duration: int = 400

@dataclass
@deserialize
class PPConfig(QOLConfig):
    window: Window = WINDOW
    change_dir_chance: float = 0.25 # can change if needed
    radius: int = 100 # maybe improvement here?
    
    pray_count: int = 100
    pred_count: int = 20
    
    grass_count: int = 2
    grass_location: list[pg.Vector2] = field(default_factory=lambda: [Vector2(100, 100), Vector2(650, 650)])

    pray_base_chance_reproduce: float = 0.1 # need polish
    pray_reproduce_pulse_timer: int = 100 # need polish

    pred_base_chance_dying: float = 0.05 # need polish
    pred_death_pulse_timer: int = 200 # need polish


class Grass(Agent):
    config: PPConfig
    id: int
    color: list[int] = [120, 235, 100, 120]
    counter: int = 0

    def on_spawn(self):
        self.config.grass_count -= 1
        self.id = self.config.grass_count
        self.pos = self.config.grass_location[self.config.grass_count]
        self.freeze_movement()
    def update(self):
        self.save_data("kind", "grass")
        if self.color[1] > 135:
            if self.counter < 10:
                self.color[1] -= 1
                self.counter = 0
            self.counter += 1
        #print(self.id, " : ", self.in_proximity_performance().filter_kind(Pray).count())

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
    config: PPConfig

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

    def before_update(self):
        super().before_update()

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    self._running = False
                if event.key == pg.K_UP:
                    self.config.fps_limit += 10
                if event.key == pg.K_DOWN:
                    self.config.fps_limit -= 10

        #print(self.config.fps_limit)

    def after_update(self):
        # Draw verything to the screen

        surface = pg.Surface((self.config.window.width, self.config.window.height), pg.SRCALPHA)
        
        target_rect = pg.Rect(0, 0, self.config.window.width, self.config.window.height)
        
        pray_counter = 0
        pred_counter = 0

        for sprite in self._all.sprites():
            if isinstance(sprite, Pray):
                pray_counter += 1
            elif isinstance(sprite, Pred):
                pred_counter += 1
            elif isinstance(sprite, Grass):
                pg.draw.circle(surface, sprite.color, sprite.pos, self.config.radius)

        self._screen.blit(surface, target_rect)

        self._all.draw(self._screen)

        pray = FONT.render("Pray count: " + str(pray_counter), True, TEXT_COLOR)
        pred = FONT.render("Pred count: " + str(pred_counter), True, TEXT_COLOR)

        self._screen.blit(pray, (0, self.config.window.height - 2 * FONT_SIZE))

        self._screen.blit(pred, (0, self.config.window.height - FONT_SIZE))

        if self.config.visualise_chunks:
            self.__visualise_chunks()

        current_fps = self._clock.get_fps()
        if current_fps > 0:
            self._metrics.fps._push(current_fps)

            if self.config.print_fps:
                fps = FONT.render("Fps: " + str(round(current_fps, 1)), True, TEXT_COLOR)
                self._screen.blit(fps, (0, 0))

        pg.display.flip()

        self._clock.tick(self.config.fps_limit)

    def __visualise_chunks(self):
        """Visualise the proximity chunks by drawing their borders."""

        colour = pg.Color(255, 255, 255, 122)
        chunk_size = self._proximity.chunk_size

        width, height = self.config.window.as_tuple()

        for x in range(chunk_size, width, chunk_size):
            vline(self._screen, x, 0, height, colour)

        for y in range(chunk_size, height, chunk_size):
            hline(self._screen, 0, width, y, colour)

