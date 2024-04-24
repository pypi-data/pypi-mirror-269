from setuptools import setup, find_packages

setup(
    name="zoltraak",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "openai",
    ],
    package_data={
        '': ['*.txt', '*.md', '*.json', '*.csv', '*.yaml', '*.yml'],
        'your_package_name': ['llms/*', 'settings/**/*'],
    },
    entry_points={
        "console_scripts": [
            "zoltraak=zoltraak.cli:main",
        ],
    },
)
