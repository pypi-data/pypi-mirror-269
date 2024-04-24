from setuptools import setup, find_packages

setup(
    name="zoltraak",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "openai",
    ],
    package_data={
        '': ['*.txt', '*.md', '*.json', '*.csv', '*.yaml', '*.yml'],
        'zoltraak': ['llms/*', 'setting/**/*'],
    },
    entry_points={
        "console_scripts": [
            "zoltraak=zoltraak.cli:main",
        ],
    },
)
