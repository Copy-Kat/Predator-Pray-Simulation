import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

import pygame as pg
from pygame.color import Color
from pygame.gfxdraw import hline, vline
from pygame.math import Vector2
from serde.de import deserialize
from vi import Agent, Config, Simulation, Window

pg.init()

ENERGY: bool = True

WIDTH: int = 750
HEIGHT: int = 750
COLLIDE_DISTANCE: int = 8  # distance between 2 agents to count as collided
BG_COLOR: tuple[int, int, int] = (0, 0, 0)  # chance bg_color if needed
TEXT_COLOR: tuple[int, int, int] = (255, 255, 255)

WINDOW: Window = Window(width=WIDTH, height=HEIGHT)

FONT_SIZE: int = 20
FONT = pg.font.SysFont("Arial", FONT_SIZE)

HUNGER_CHANGE = 1 if ENERGY else 0


@dataclass
@deserialize
class QOLConfig(Config):
    visualise_chunks: bool = True
    print_fps: bool = True
    duration: int = 0


@dataclass
@deserialize
class PPConfig(QOLConfig):
    window: Window = WINDOW
    change_dir_chance: float = 0.25  # can change if needed
    radius: int = 100  # maybe improvement here?

    pray_count: int = 100
    pred_count: int = 10

    grass_count: int = 3
    grass_location: list[pg.Vector2] = field(
        default_factory=lambda: [Vector2(100, 100), Vector2(650, 650), Vector2(100, 650)]
    )
    grass_max_cap: int = 1500
    grass_natural_regen_rate: int = 10
    grass_damaged_timer: int = 100

    pray_base_chance_reproduce: float = 0.1  # need polish
    pray_reproduce_pulse_timer: int = 100  # need polish
    pray_grass_consumption: int = 1

    pred_base_chance_dying: float = 0.001  # need polish
    pred_death_pulse_timer: int = 200  # need polish


class Grass(Agent):
    config: PPConfig
    id: int
    color: int = 235
    counter: int = 0
    current_cap: int
    max_cap: int
    damaged: bool = False

    def on_spawn(self):
        self.config.grass_count -= 1
        self.id = self.config.grass_count
        self.pos = self.config.grass_location[self.config.grass_count]
        self.max_cap = self.config.grass_max_cap
        self.current_cap = self.config.grass_max_cap
        self.freeze_movement()

    def update(self):
        self.save_data("kind", "grass")

        if not self.damaged:
            pray_in_range = list(self.in_proximity_accuracy().without_distance().filter_kind(Pray))
            current_cap = (
                self.current_cap
                - len(pray_in_range) * self.config.pray_grass_consumption
                + self.config.grass_natural_regen_rate
            )
            if current_cap > 0:
                self.current_cap = min(current_cap, self.max_cap)
                self.color = 135 + int((self.current_cap / self.max_cap) * 100)
            else:
                # for pray in pray_in_range:
                # pray.kill()
                self.damaged = True
                self.regen_timer = self.config.grass_damaged_timer

            return

        if self.regen_timer == 0:
            self.damaged = False

        self.regen_timer -= 1

        # print(self.id, " : ", self.in_proximity_performance().filter_kind(Pray).count())


class PrayStates(Enum):
    SEARCHING = auto()
    STILL = auto()
    RUNAWAY = auto()


# Pray class
class Pray(Agent):
    config: PPConfig
    reproduce_timer: int = 100  # time between each reproduce attempt
    hunger: float = 100
    state: PrayStates = PrayStates.SEARCHING
    still_walk_timer: int
    pred_pos: Vector2

    def update(self):
        self.save_data("kind", "Pray")  # save data for later

        in_range = list(self.in_proximity_accuracy())

        pred_in_range = [pred for pred in in_range if isinstance(pred[0], Pred) and pred[1] < 70]

        if pred_in_range:
            self.state = PrayStates.RUNAWAY
            self.pred_pos = pred_in_range[0][0].pos
            return

        elif self.state == PrayStates.SEARCHING:
            grass_in_range = [
                grass for grass in in_range if isinstance(grass[0], Grass) and not grass[0].damaged
            ]

            if grass_in_range:
                self.state = PrayStates.STILL
                self.move = (grass_in_range[0][0].pos - self.pos).normalize()
                self.still_walk_timer = random.randint(10, 30)
        else:
            grass_in_range = [grass for grass in in_range if isinstance(grass[0], Grass)]

            if grass_in_range:
                if grass_in_range[0][0].damaged:
                    self.state = PrayStates.SEARCHING
                    self.move.rotate_ip(180)

        if self.reproduce_timer == 0:
            if self.hunger > 50:
                p = random.random()

                # reproduce
                if self.config.pray_base_chance_reproduce > p:
                    prng = self.shared.prng_move
                    self.reproduce()

                    self.move.rotate_ip(prng.uniform(-10, 10))

            # reset timer regardless
            self.reproduce_timer = self.config.pray_reproduce_pulse_timer
            return

        self.reproduce_timer -= 1
        self.hunger -= HUNGER_CHANGE

    def change_position(self):  # basic random move
        changed = self.there_is_no_escape()

        if changed:
            self.state = PrayStates.SEARCHING

        if self.state == PrayStates.RUNAWAY:
            self.move = self.pos - self.pred_pos

        elif self.state == PrayStates.STILL:
            if self.still_walk_timer == 0:
                self.hunger = min(self.hunger + 2, 100)
                return
            self.still_walk_timer -= 1
        else:
            prng = self.shared.prng_move

            should_change_dir = prng.random()

            if self.config.change_dir_chance > should_change_dir:
                self.move.rotate(prng.uniform(-10, 10))

        self.pos += self.move.normalize()


# Pred class
class Pred(Agent):
    config: PPConfig
    target: Pray
    death_timer: int
    hunger: int = 100
    dying: bool = False

    def update(self):
        self.save_data("kind", "Pred")  # save data

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

        self.hunger -= HUNGER_CHANGE

    def change_position(self):
        self.there_is_no_escape()

        # aquire target
        targets = list(self.in_proximity_accuracy().filter_kind(Pray))

        if targets:  # if target found
            targets = sorted(targets, key=lambda x: x[1])  # sort targets

            self.target = targets[0][0]  # get closest target

            if (self.target.pos - self.pos).length() < COLLIDE_DISTANCE:
                self.target.kill()  # kill if collided
                self.hunger = 100
                if self.dying:
                    self.dying = False
                self.pos += self.move
                return

            self.move = self.target.pos - self.pos

        else:  # random walk
            prng = self.shared.prng_move

            should_change_dir = prng.random()

            if self.config.change_dir_chance > should_change_dir:
                self.move.rotate(prng.uniform(-10, 10))

        self.pos += self.move.normalize() * 2  # make pred faster than prey


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

        # print(self.config.fps_limit)

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
                pg.draw.circle(
                    surface, (120, sprite.color, 100, 120), sprite.pos, self.config.radius
                )

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
