from setuptools import setup, find_packages
import os
import sys

# zoltraakディレクトリのパスを取得
zoltaak_dir = os.path.dirname(os.path.abspath(__file__))

# zoltraakディレクトリ内のすべてのファイルを取得
package_data = []
for root, dirs, files in os.walk(zoltaak_dir):
    for file in files:
        package_data.append(os.path.join(root, file))

setup(
    name="zoltraak",
    version="0.1.9",
    packages=find_packages(),
    # package_dir={'': '.'},  # ここでベースディレクトリを指定
    install_requires=[
        "openai",
        "anthropic",
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
