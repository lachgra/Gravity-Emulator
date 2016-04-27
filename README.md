Physics-Emulator
================

Rudimentary physics emulator written in Python.
Uses the event-driven Pygame library to implement gravity, and basic Newtonian mechanics.


Controls:

UP    - Apply an upward force

DOWN  - Apply a downward force

RIGHT - Apply a force to the right

LEFT  - Apply a force to the left

SPACE - Resets all particles to a random location within the frame

SHIFT - Introduces random ax and ay values for all particles


g - Introduce or remove a gravitational field

r - Introduce a rainbow like random colour scheme on the particles (epilepsy warning)

c - Introduce a new background colour scheme

q - Quit the emulator

Possible interesting features:

- [Done] A central mass of which the particles are gravitationally attracted to
- [Done] Make all particles attracted to each other
- A collision detection system of individual particles with respect to each other
- A bar on which the particles can sit, of which can be tilted, changing their acceleration
