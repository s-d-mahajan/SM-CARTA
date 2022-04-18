from setuptools import setup

setup(
    name="SM-CARTA",
    version="0.1.0",
    py_modules=["captable"],
    install_requires=[
        "Click",
        "pytest",
        "coverage",
    ],
    entry_points={
        "console_scripts": [
            "captable = captable.scripts.cli:captable",
        ],
    },
)
