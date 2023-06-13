from typing import Tuple, List

from fastapi import FastAPI
from pydantic import BaseModel

from tower_defense.block import Block
from tower_defense.tower_defense_controller import TowerDefenseController


class Position(BaseModel):
    x: float
    y: float


def add_routes(app: FastAPI, controller: TowerDefenseController) -> FastAPI:
    @app.get("/")
    async def home() -> List[str]:
        return [route.path for route in app.routes]

    @app.get("/map/shape")
    async def get_map_shape() -> Tuple[int, int]:
        return controller.map_shape()

    @app.get("/blocks")
    async def get_blocks() -> List[Tuple[Tuple[int, int], Block]]:
        return list(controller.iter_blocks())

    @app.get("/towers")
    async def get_towers() -> List[Tuple[float, float]]:
        return [tower.get_position() for tower in controller.iter_towers()]

    @app.get("/monsters")
    async def get_monsters() -> List[Tuple[float, float]]:
        return [monster.get_position() for monster in controller.iter_monsters()]

    @app.get("/projectiles")
    async def get_projectiles() -> List[Tuple[float, float]]:
        return [
            projectile.get_position() for projectile in controller.iter_projectiles()
        ]

    @app.get("/player/health")
    async def get_player_health() -> int:
        return controller.get_player_health()

    @app.post("/spawn/start")
    async def start_spawning_monster() -> bool:
        return controller.start_spawning_monsters()

    return app
