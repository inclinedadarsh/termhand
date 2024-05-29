from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="termhand",
    version="0.2.1",
    install_requires=[
        "google-generativeai",
    ],
    entry_points="""
        [console_scripts]
        th=th:main
    """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Adarsh Dubey",
    author_email="dubeyadarshmain@gmail.com",
    description="A command-line tool that generates terminal commands from natural language prompts.",
    url="https://github.com/inclinedadarsh/termhand",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
