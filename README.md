# Ant Colony Simulation

A Python/Pygame simulation of ants moving between a nest and food while leaving two pheromone fields. The fields diffuse and decay over time, allowing the agents to react to trails rather than follow fixed paths.

## Running

Install the two runtime dependencies:

```text
pip install numpy pygame
python main.py
```

The default setup opens an 800 by 600 Pygame window, creates 50 ants, and advances the simulation one millisecond at a time.

## Code map

- `ant.py` contains agent movement and behaviour.
- `grid.py` stores the nest, food map, and pheromone arrays.
- `simulation.py` updates agents, diffuses and decays pheromones, and draws the state.
