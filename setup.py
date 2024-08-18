from setuptools import setup

setup(
    name="taskly",
    version="1.0.0",
    description="A CLI application to manage tasks.",
    author="Ahmed",
    author_email="braika7med@gmail.com",
    url="https://github.com/brkahmed/taskly",
    py_modules=["taskly"],
    entry_points={
        "console_scripts": [
            "taskly=taskly:main",
        ],
    },
    install_requires=[
        "tabulate",
    ],
    tests_require=[
        "pytest",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
