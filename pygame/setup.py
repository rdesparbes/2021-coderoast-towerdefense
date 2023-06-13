from setuptools import setup, find_packages


setup(
    name="tower-defense-pygame",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pygame",
    ],
    entry_points={
        "tower_defense.views": [
            "pygame_view = tower_defense_pygame.view_launcher",
        ],
    },
)
