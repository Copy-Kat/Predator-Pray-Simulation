# Methodology:

Most of logic are made using finite-state machine

## Pray:
3 states: SEARCHING, STILL and RUNAWAY:

- SEARCHING: Effectively random walk: take 1 direction, keep moving. Sometime changes direction
- STILL: complete standstill, not moving
- RUNAWAY: run in opposite direction of predator

State changes:
- SEARCHING -> STILL: agent collide with a patch of grass, will reach standstill after some random number of steps
- STILL -> SEARCHING: the patch of grass agent is on has no grass left. Agent take the center of grass patch and walk in opposite direction
- SEARCHING / STILL -> RUNAWAY: agent detect that there is predator in range. Agent take the position of predator and run in opposite direction
- RUNAWAY -> ANY: by default, RUNAWAY will always go to SEARCHING after agent has detected that there are no predator in range.
- From here, the agent is free to remain in SEARCHING or transition to STILL if it has found some grass.

- Energy system: Hunger bar - start at 100, consume 1 every tick, if on grass then regen 2 every tick

Reproduction:
- This is taken seperately from the other states as it is a sub process rather than a whole state.
- An internal timer will start at the start of the simulation.
- Once the timer reach 0, the agent will roll a number from 0 to 1 and check against a fixed constant. If the number is larger and the agent has sufficient energy (> 50 as of now), it ill reproduce.
- One note: if the agent is in RUNAWAY state, the timer will not tick and will continue once the agent go out of  RUNAWAY state

Death:
- Pray cannot die.

## Predator: These are the idea, some of them are not yet implemented
- 2 States: CHASING and HUNTING and 1 internal status Death Door:

- HUNTING: Agent will start in this state, normal movement speed (the move speed difference is not yet implemented). Agent scout around to see if it can find any Pray
- CHASING: Agent found (a) pray in its range, lock on to the pray and move in that specific direction. (Move speed here should be faster but not implemented).
- Once the pray is caught, the pray is killed and the agent return to HUNTING

- Energy system: Hunger bar - start at 100, consume 1 every tick, go back to full after 1 kill

- Death Door is a special status as its mimic the starvation process. Kick in once the hunger bar reach 0
- A timer will start upon entering Death Door.
- The agent can still hunt or chase as normal.
- If a pray is consumed, the agent will lose this status and return to normal.
- But if the timer is let to tick to 0, every tick from here, the agent is call a RNG to check its chance of death. If success, it will die.
- Even in this state, if the agent can kill a pray, it will still return to normal.

State changes:
- HUNTING -> CHASING: Agent found a target in range, initiate lock in and enter chase mode.
- CHASING -> HUNTING: Agent killed the target, now going back to HUNTING mode
- Note that the agent could always be in CHASING mode as once it is in HUNTING mode, it can find a new pray imediately and enter CHASING mode again.

Reproduction: Predator cannot reproduce (as of now)

## Grass:
2 states: Damaged and Undamaged?

- Grass started with a certain cappacity and in the Undamaged state.
- In this state, every tick, the agent will count the number of pray on top of it can calculate the new cappacity accordingly.
- The agent is also allowed to have a certain rate of natural regen which will be used in the calculation of the new capacity.
- Once the capacity reach 0, the agent is enter the Damaged state.
- In this state, the cappacity of the agent will be locked at 0 and a timer will start.
- Until the timer reach 0, it will not ba able to regen its cappacity.
- Once the timer is at 0, it will go back to the Undamaged state.
- Note: it is possible to constantly be in Damaged state as if the agents refused to leave the patch, any new regen will be eaten and it will go back to being Damaged.

State changes:
- Too simple and obvious so I will not add it here.

