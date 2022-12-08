import math

from tower_defense.interfaces.entity import IEntity


def distance(entity_a: IEntity, entity_b: IEntity) -> float:
    return math.dist(entity_a.get_position(), entity_b.get_position())
