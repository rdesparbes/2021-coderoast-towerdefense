from setuptools import setup, find_packages


setup(
    name="tower-defense",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "tower_defense.views": "tkinter_view = tower_defense.view.view_launcher[tk]",
        "console_scripts": [
            "TowerDefense=tower_defense.scripts.game:main",
        ],
    },
    install_requires=[],
    extras_require={
        "tk": ["tk", "Pillow"],
        "dev": [
            "pytest",
            "black",
            "types-pillow",
            "types-setuptools",
        ],
    },
)
