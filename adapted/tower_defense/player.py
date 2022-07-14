from dataclasses import dataclass


@dataclass
class Player:
    money: int = 5_000_000
    health: int = 100
