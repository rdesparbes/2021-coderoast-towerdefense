from setuptools import setup, find_packages


setup(
    name="tower-defense",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "TowerDefense=tower_defense.scripts.game:main",
        ],
    },
    install_requires=["tk", "Pillow"],
    extras_require={
        "dev": [
            "pytest",
            "black",
        ]
    },
)
