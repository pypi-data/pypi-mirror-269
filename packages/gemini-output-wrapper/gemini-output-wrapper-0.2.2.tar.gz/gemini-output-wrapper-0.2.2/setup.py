from setuptools import setup, find_packages

setup(
    name="gemini-output-wrapper",
    version="0.2.2",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "importlib",
        "typing",
        "google-generativeai",
        "inspect",
    ],
    description="Library for wrapping Gemini API output with Json and Python objects",
    author="Min Htet Naing",
    author_email="minhtetnaing25mhn@gmail.com",
    url="https://github.com/Osbertt-19/gemini-output-wrapper.git",
)
