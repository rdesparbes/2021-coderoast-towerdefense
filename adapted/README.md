# Tower Defense: Refactored

## Rules

For this refactor, a certain number of rules have been followed.

It is forbidden to:
- Modify the behavior of the game
- Modify the design of the GUI
- Modify the existing resources and their organization

Only the python files can be modified.

## What does this refactor unlock?

- The logic of the game and the view are now decoupled. It would be possible to implement 
  another view that does not use Tkinter, that interacts with the `TowerDefenseController`
  (see [](tower_defense/tower_defense_controller.py)).
- The desired FPS can be changed, and the speed at which the entities evolve is not dependent
  on the frame rate. The game can now be played at a higher FPS than the default of 20 FPS,
  without changing the speed of the projectiles and monsters (see [](tower_defense/constants.py))
- The monsters, the towers and the projectiles have been split in multiple concepts so that
  they are entirely customizable: effects, damages, fire rates, upgrades... New towers, 
  projectiles and monsters can be defined, and it would be possible to store those definitions 
  in an external configuration file (see [](tower_defense/entities/default)).
- The map view can now be composed of rectangular tiles of arbitrary size (see [](tower_defense/view/game_objects/map.py))
