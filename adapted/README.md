# Tower Defense: Refactored

## Install

```shell
pip install -e .[tk]
TowerDefense
```

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
  (see [this file](tower_defense/tower_defense_controller.py)).
- The desired FPS can be changed, and the speed at which the entities evolve is not dependent
  on the frame rate. The game can now be played at a higher FPS than the default of 20 FPS,
  without changing the speed of the projectiles and monsters (see [this file](tower_defense/view/game_objects/view.py))
- The monsters, the towers and the projectiles have been split in multiple concepts so that
  they are entirely customizable: effects, damages, fire rates, upgrades... New towers, 
  projectiles and monsters can be defined, and it would be possible to store those definitions 
  in an external configuration file (one for the [monsters](tower_defense/core/monster/default.py) and one for the
  [towers](tower_defense/core/tower/default.py)).
- The map view can now be composed of rectangular tiles of arbitrary size (see [this file](tower_defense/view/game_objects/map.py))
- A system of plugin has been added to add new custom `View`s. The game can handle multiple `View`s at once,
  and each `View` can receive information from the game logic, and act on the game. A default `View` is available
  in this package with the original behavior, implemented with *tkinter*. Additional views can be implemented
  as Python plugins to replace the GUI or to implement a bot for example.

## How to register a new `View`?

To do that, one must create a Python package that implements the `tower_defense.views` entrypoint. 
This entrypoint must lead to a module that calls the `tower_defense.interfaces.views.register_view_launcher`
function on the custom `View` to register. An example is available in the `bot` folder.
