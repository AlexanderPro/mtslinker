from setuptools import setup, find_packages

setup(
    name='mtslinker',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'httpx>=0.27.2',
        'moviepy>=1.0.3',
        'tqdm>=4.66.6',
    ],
    entry_points={
        'console_scripts': [
            'mtslinker=mtslinker.cli:main',
        ],
    },
    python_requires=">=3.9",
)
