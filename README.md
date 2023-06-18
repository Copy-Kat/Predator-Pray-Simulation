# Predator-Pray-Simulation

A simple predator and pray simulation built for the Project Collective Inteligence course using the [violet](https://github.com/m-rots/violet) engine and Pygame as the backend

## Files:
- main.py: the driver code for the simulation, only include code to start the simulation. Cannot change the parameters in main yet as it would cause circular imports. May change later by using TOML files.
- lib.py: conatin all the logic for the agents and the config of the simulation
- stats.py: do statistical analysis on the data (TODO: add graphs)

## Rules:
2 agent types: Predator and Pray (Will be more complex later)

### Predators:
- Start by wandering around randomly
- For each tick, look around the proximity for a pray and lock on to it
- Once locked in, it will only move towards the pray
- If the 2 collide, the pray is killed and the predator try to find a new pray again
- If durring chase, the predator found a closer pray, it will lock on to the new target instead
- If there are no targets then random walk

### Pray:
- Always walk randomly

### Spontaneous death:
- Pred has a small chance to suddenly die. This chance is lowered if pred keep eating pray 
- The chance will slowly rise if wolf no eat -> eat to survive
- Pray cannot die (assumption)

### Reproduction:
- Pray has a small chance to commit cell division (1 split into 2)
- Pred cannot reproduce (assumption)

## Constants:

- Colision distance: 8px - each sprite is a circle with a diameter of 8px -> collision if distance between 2 agents is less than 8px

## Dynamic Variables:

- Frame rate a.k.a sim speed: adjust during simulation to speed up or slow down (To be implemented)

## Initial Prameters: Adjust at will
- Bounding box: 750 x 750 - could be adjusted for testing
- Reproduce chance: 0.001 - CHANGE THIS TOO HIGH WILL CRASH YOUR COMPUTER ("breed like rabits")
- Random pred death chance: 0.005 - too high and wolf die before eating anything
- Death chance increase: 0.0001 - too high and wolf die before eat

## TODO: first 3 are manditory, rest are nice to have
- [x] Implement the basic bare-bone simulation (Basically done, just need polishing)
- [ ] Build plots for population changes (Will be complete after understanding Polars)
- [ ] Energy system for Pred, could be modeled as hunger?
- [ ] Study diff between with and without hunger
- [ ] Add grass
- [ ] Add flocking
- [ ] Add sexual reproduction (no more cell division)
- [ ] Add aging
- [ ] Make more complex environment
