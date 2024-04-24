from setuptools import setup, find_packages

setup(
    name="zoltraak",
    version="0.1.12",
    packages=find_packages(),
    # package_dir={'': '.'},  # ここでベースディレクトリを指定
    install_requires=[
        "openai",
        "anthropic",
        "groq",
        "python-dotenv",  # 追加
        "pyperclip",  # 追加


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
