# Predator-Pray-Simulation

A simple predator and pray simulation built for the Project Collective Inteligence course using the [violet](https://github.com/m-rots/violet) engine and Pygame as the backend

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

## Constants:

- Colision distance: 8px - each sprite is a circle with a diameter of 8px -> collision if distance between 2 agents is less than 8px

## Dynamic Variables:

- Frame rate a.k.a sim speed: adjust during simulation to speed up or slow down 

## Initial Prameters:
- Bounding box: 750 x 750 - could be ajust for testing

