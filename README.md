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
2 agent types: Predator and Pray (Will be more complex later)

### Predators:
- Start by wandering around randomly.
- For each tick, look around the proximity for a pray and lock on to it.
- Once locked in, it will only move towards the pray.
- If the 2 collide, the pray is killed and the predator try to find a new pray again.
- If durring chase, the predator found a closer pray, it will lock on to the new target instead.
- If there are no targets then random walk.
- The speed of the predator will be faster than pray.

### Pray:
- Always walk randomly.

### Hunger (Enegry system):
- The pred has a hunger bar now, staring at 100 and decrease 1 per tick.
- Eating a pray refill the bar to full.

### Spontaneous death:
- Pred has a small chance to suddenly die.
- If the pred has no hunger bar left, they enter the dying state.
- In this state, they have a timer to find more food.
- If the timer reach 0, the chance will be rolled every tick, potentially killing them.
- Pray cannot die (assumption).

### Reproduction:
- Pray has a small chance to commit cell division (1 split into 2).
- Every pray will have a timer to the next reproduction attempt.
- Once the timer reach 0, they roll a chance to birth a new pray.
- The original agent will change direction by 90 degrees if gave birth (only here for testing, will change later).
- In both cases the timer will be reset.
- Pred cannot reproduce (assumption).

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
- [ ] Build plots for population changes (Will be complete after understanding Polars)
- [x] Energy system for Pred, could be modeled as hunger? (Need polishing on parameters)
- [ ] Study diff between with and without hunger
- [ ] Add grass
- [ ] Add flocking
- [ ] Add sexual reproduction (no more cell division)
- [ ] Add aging
- [ ] Make more complex environment

## Points of improvement: (Nice to have, not manditory)
- [ ] Somehow make predator to have 2 proximities: hunt mode and chase mode (hunt is larger than chase)
- [ ] Following last point, make variable speed for both modes (hunt is slower than chase)
- [ ] Make pray aware of the pred and run away
