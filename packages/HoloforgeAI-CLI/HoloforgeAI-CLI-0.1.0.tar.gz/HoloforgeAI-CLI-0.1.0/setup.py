from setuptools import setup, find_packages

setup(
    name="HoloforgeAI-CLI",
    version="0.1.0",
    author="Erik Rowan <erik@holoforge.ai, Gerardo I. Ornelas <gerardo@holoforge.ai>",
    author_email="erik@holoforge.ai",
    description="A CLI companion tool for managing Holoforge applications",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/holoforgeai/holoforge-cli",  # Optional
    packages=find_packages(),
    install_requires=[
        'boto3',
        'requests',
        'configparser',  # Make sure all your dependencies are listed here
    ],
    entry_points={
        'console_scripts': [
            'holo=holoforgecli.holo:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
