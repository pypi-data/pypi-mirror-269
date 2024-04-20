from setuptools import setup, find_packages

setup(
    name='discord_controler',
    version='1',
    packages=find_packages(),
    install_requires=[
        'Flask',
    ],
    author='mao',
    author_email='your@email.com',
    description='A module for controlling a Discord bot via a web server.',
    url='https://github.com/yourusername/discord-control',
)
