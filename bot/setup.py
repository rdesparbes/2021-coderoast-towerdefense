from setuptools import setup, find_packages


setup(
    name="bot",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "tower_defense.views": [
            "bot_view = bot.view_launcher",
        ],
    },
    install_requires=["tower-defense"],
)
