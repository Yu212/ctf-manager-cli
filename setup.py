from setuptools import setup

setup(
    name="cm-cli",
    version="0.1.0",
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "cm = cm.cli:cli",
        ],
    },
)
