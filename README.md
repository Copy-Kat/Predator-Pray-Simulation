# Predator-Pray-Simulation

A simple predator and pray simulation built for the Project Collective Inteligence course using the [violet](https://github.com/m-rots/violet) engine and Pygame as the backend. The graphs and data analysis is done with Polars and Plotly

## Getting started:
Clone the repository: 
```bash
git clone https://github.com/Copy-Kat/Predator-Pray-Simulation.git
```
Or clone using Github Desktop

Install the dependencies:
```python
pip install polars pyarrow pandas plotly
```

Have a look at lib.py to use a custom config for the simulation

Run the simulation:
```bash
python main.py
```

Analyse data:

Open a jupyter notebook client in the current directory:
```bash
jupyter
```
Or
```bash
jupyter lab
```

Run all the cells in the notebook to see all the graphs and data analysis

## Files:
- main.py: the driver code for the simulation, only include code to start the simulation. Cannot change the parameters in main yet as it would cause circular imports. May change later by using TOML files.
- lib.py: conatin all the logic for the agents and the config of the simulation.
- stats.py / stats.ipynb: do statistical analysis on the data. Python file for cleaning and preping data, Notebook for visualize graphs.

## Rules:
3 agent types: Predator and Pray and Grass (Will be more complex later)

### Predators:
- Start out with random walk.
- If it find a pray within range, it will lock on to the target.
- Once locked on, the it will move specifically towards that direction. (chasing the pray)
- If during chase, it find another pray that is closer, it will lock on to that target instead.
- The chase is considered successful if it managed to collide with the pray.
- On collision, it will consume and kill the pray.
- The energy system is designed as a hunger bar.
- The bar starts at 100 and reduces every frame depend on how much enery it consumes.
- Once the bar hit 0, it will enter sudden death mode.
- In this mode, a timer will start, if it managed to find and eat a pray, it will go back to normal.
- If the timer run out, a RNG will run every tick, if successful, it will die.
- Within the current impl, each tick will consume 1 energy and eating a pray restore to full.
- As of now, there is no way for it to reproduce.
- By design, it will be faster than pray though the number can be modified

### Pray:
- The pray has 3 states: RUNAWAY > STILL > SEARCHING
- Start out with random walk. (SEARCHING)
- If it find a patch of grass, it will attempt to move towards the center, entering STILL state.
- The number of steps is randomly determined within a range.
- Once the steps are fullfiled, it will stop and eat the grass.
- In both states (SEARCHING and STILL), if it detect that there is a predator in range, it will go into RUNAWAY state.
- In this state, it will take the position of the predator and run in the exact opposite direction, maximizing survival chance.
- If it detect that there are no predator in range, it will go back to 1 of the other 2 states, which ever takes priority and whether or not the conditions are met.
- If the agent is in the still state, it will continue to stay in this state untill there is no grass left to eat.
- If there are no grass left, it will take the center position of the patch of grass and move in the exact opposite direction.
- If the agent is not in RUNAWAY state, there will be an internal timer counting down.
- Once the timer reach 0, it will check the RNG and its own hunger bar.
- If the condition is met, it will reproduce another pray.
- As of now, pray cannot die of natural causes, it can only die by being eaten.

### Grass:
- Represented as a circular patch of grass.
- It start out with a certain capacity.
- Every tick, it will count the number of pray on top of it and calculate the new capacity.
- This calculation will also take natural regen into account.
- Once the capacity fall to 0, it will enter the Damaged state.
- In this state, an internal timer will start ticking.
- Until the timer reach 0, this patch of grass will not generate.
- After the timer is done, it can then regen the capacity as usual.
- The color of the grass is dynamically changed to match the current cappacity.

## Constants:
- Colision distance: 8px - each sprite is a circle with a diameter of 8px -> collision if distance between 2 agents is less than 8px.

## Dynamic Variables:
- Frame rate a.k.a sim speed: adjust during simulation to speed up or slow down (To be implemented).

## Initial Prameters: Adjust at will
| Parameters     | Values          |
|--------------- | --------------- |
| Bounding Box | 750 x 750 |
| Pray reproduce chance | 0.25 |
| Pray reproduce cycle | 100 |
| Pred dying chance | 0.1 |
| Pray death door timer | 100 |

## Expected results:
A dynamic shift in population for both predator and pray overtime. Predators would start with an abundance of food which lead to them thriving and exhausting the food source (pray pops reduced). With less food to go around, predators would die out one by one (pred pops reduced), leaving room for pray to reproduce (pray pops increased). With the left over pred, now with an abundance of food again, could begin to thrive and restart the cycle.

## Current problems:
- Pray cannot die while predators could. Pray could reproduce but predators could not. This lead to a quick 1 cycle of the simulation rather than a contineous cycle. Not sure if this is intended as asexsual reproduction is an idea but not manditory.

## TODO: first 3 are manditory, rest are nice to have
- [x] Implement the basic bare-bone simulation (Basically done, just need polishing)
- [ ] Build plots for population changes (Kinda done?)
- [x] Energy system for Pred, could be modeled as hunger? (Need polishing on parameters)
- [ ] Study diff between with and without hunger
- [ ] Add grass (Actually kinda working)
- [ ] Add flocking
- [ ] Add sexual reproduction (no more cell division)
- [ ] Add aging
- [ ] Make more complex environment

## Points of improvement: (Nice to have, not manditory)
- [ ] Somehow make predator to have 2 proximities: hunt mode and chase mode (hunt is larger than chase)
- [ ] Following last point, make variable speed for both modes (hunt is slower than chase)
- [ ] Make pray aware of the pred and run away
