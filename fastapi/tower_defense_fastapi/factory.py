from typing import Tuple, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from tower_defense.block import Block
from tower_defense.interfaces.tower import ITower
from tower_defense.interfaces.tower_view import ITowerView
from tower_defense.tower_defense_controller import TowerDefenseController


class Position(BaseModel):
    x: float
    y: float


def add_routes(app: FastAPI, controller: TowerDefenseController) -> FastAPI:
    @app.get("/")
    async def home() -> List[str]:
        return [route.path for route in app.routes]

    @app.get("/player/health")
    async def get_player_health() -> int:
        return controller.get_player_health()

    @app.get("/player/money")
    async def get_player_money() -> int:
        return controller.get_player_money()

    @app.post("/block")
    async def get_block(
        world_position: Tuple[float, float]
    ) -> Tuple[Tuple[int, int], Block]:
        return controller.get_block(world_position)

    # @app.post("/tower")
    # async def get_tower(tower_position: Tuple[int, int]) -> Optional[ITower]:
    #     return controller.get_tower(tower_position)

    @app.get("/tower_views")
    async def get_tower_view_names() -> List[str]:
        return controller.get_tower_view_names()

    # @app.post("/tower_view")
    # async def get_tower_view(tower_view_name: str) -> ITowerView:
    #     return controller.get_tower_view(tower_view_name)

    @app.get("/blocks")
    async def iter_blocks() -> List[Tuple[Tuple[int, int], Block]]:
        return list(controller.iter_blocks())

    @app.get("/map/shape")
    async def map_shape() -> Tuple[int, int]:
        return controller.map_shape()

    @app.get("/spawn/ready")
    async def can_start_spawning_monsters() -> bool:
        return controller.can_start_spawning_monsters()

    @app.post("/spawn/start")
    async def start_spawning_monster() -> bool:
        return controller.start_spawning_monsters()

    @app.post("/tower/build")
    def try_build_tower(
        tower_view_name: str, world_position: Tuple[float, float]
    ) -> bool:
        return controller.try_build_tower(tower_view_name, world_position)

    @app.post("/tower/upgrade")
    def upgrade_tower(tower_position: Tuple[int, int]) -> None:
        controller.upgrade_tower(tower_position)

    @app.get("/tower/sell")
    def sell_tower(tower_position: Tuple[int, int]) -> None:
        controller.sell_tower(tower_position)

    @app.get("/towers")
    async def iter_towers() -> List[Tuple[float, float]]:
        return [tower.get_position() for tower in controller.iter_towers()]

    @app.get("/monsters")
    async def iter_monsters() -> List[Tuple[float, float]]:
        return [monster.get_position() for monster in controller.iter_monsters()]

    @app.get("/projectiles")
    async def iter_projectiles() -> List[Tuple[float, float]]:
        return [
            projectile.get_position() for projectile in controller.iter_projectiles()
        ]

    return app
