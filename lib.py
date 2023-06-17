from dataclasses import dataclass
from vi import Agent

class Pray(Agent):
    
    def change_position(self):

        self.there_is_no_escape()

        self.pos += self.move

class Pred(Agent):
    lock_on: bool = False
    target: Pray

    def update(self):
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
