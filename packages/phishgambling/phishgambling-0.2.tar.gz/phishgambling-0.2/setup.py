from setuptools import setup, find_packages

setup(
    name="phishgambling",
    description="This project is for film project only.",
    version="0.2",
    author="Jan Leander",
    packages=find_packages(),
    install_requires=[
        # add dependencies here.
        # e.g 'num>=1.11.1'
    ],
    entry_points={
        "console_scripts": [
            "generate_phish = phishgambling:main",
        ],
    },
)
