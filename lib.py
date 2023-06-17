from dataclasses import dataclass
from serde.de import deserialize
from vi import Agent, Window, Config
import random


WIDTH: int = 750
HEIGHT: int = 750

WINDOW: Window = Window(width=WIDTH, height=HEIGHT)

@dataclass
@deserialize
class PPConfig(Config):
    window: Window = WINDOW
    pray_base_chance_reproduce: float = 0.002 # THIS IS DANGEROUS, CHANGE AT YOUR OWN DISCRETION
    pred_base_chance_dying: float = 0.005 # TOO LOW AND WOLF DIE TOO FAST
    d_pred_clock: float = 0.0001

class Pray(Agent):
    config: PPConfig

    def update(self):
        self.save_data("kind", "Pray")
        p = random.uniform(0, 1)

        if p < self.config.pray_base_chance_reproduce:
            self.reproduce()

            self.move.rotate_ip(90)

    
    def change_position(self):

        self.there_is_no_escape()

        self.pos += self.move

class Pred(Agent):
    config: PPConfig
    lock_on: bool = False
    target: Pray
    d_clock: float = 1

    def update(self):

        self.save_data("kind", "Pred")

        p = random.uniform(0, 1)

        if p > self.config.pred_base_chance_dying + self.d_clock:
            self.kill()
            return
        
        self.d_clock -= self.config.d_pred_clock
        
        if not self.lock_on:
            target = self.in_proximity_performance().filter_kind(Pray).first()
            if target is not None:
                self.target = target
                self.lock_on = True

    def change_position(self):

        #print(self.config)

        self.there_is_no_escape()

        targets = list(self.in_proximity_accuracy().filter_kind(Pray))

        if targets:
        
            targets = sorted(targets, key = lambda x : x[1])

            self.target = targets[0][0] 
        
            if (self.target.pos - self.pos).length() < 8:
                self.target.kill()
                self.lock_on = False
                self.pos += self.move
                return

            self.move = (self.target.pos - self.pos).normalize()

        self.pos += self.move
