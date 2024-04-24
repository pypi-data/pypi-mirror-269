from setuptools import setup, find_packages

setup(
    name="zoltraak",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
    ],
    entry_points={
        "console_scripts": [
            "zoltraak=zoltraak.cli:main",
        ],
    },
)
