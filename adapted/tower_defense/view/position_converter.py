from typing import Tuple


class PositionConverter:
    def __init__(self, block_shape: Tuple[int, int]):
        self.block_shape = block_shape

    def position_to_pixel(self, position: Tuple[float, float]) -> Tuple[int, int]:
        return (
            int(position[0] * self.block_shape[0]) + self.block_shape[0] // 2,
            int(position[1] * self.block_shape[1]) + self.block_shape[1] // 2,
        )

    def pixel_to_position(self, pixel: Tuple[int, int]) -> Tuple[float, float]:
        return pixel[0] / self.block_shape[0], pixel[1] / self.block_shape[1]

    def world_vector_to_screen_vector(
        self, in_world_vector: Tuple[float, float]
    ) -> Tuple[int, int]:
        return (
            int(in_world_vector[0] * self.block_shape[0]),
            int(in_world_vector[1] * self.block_shape[1]),
        )
