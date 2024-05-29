from setuptools import setup

setup(
    name="TermHand",
    version="0.",
    py_modules=["th"],
    install_requires=[
        "google-generativeai",
    ],
    entry_points="""
        [console_scripts]
        th=th:main
    """,
)
