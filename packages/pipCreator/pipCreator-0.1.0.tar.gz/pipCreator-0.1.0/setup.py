from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pipCreator",
    version="0.1.0",
    description="This creates all the necessary files for creating a python package.",
    author="Rakesh Kanna",
    author_email='rakeshkanna0108@gmail.com',
    licence="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=["pip", "package", "python", "setup", "create", "creator"],
    python_requires=">=3.6",
    project_urls={
        'GitHub': 'https://github.com/rakeshkanna-rk/pipCreator/',
        'PyPI' : 'https://pypi.org/project/pipCreator/'
    },
    install_requires=[
        "click", 
        "colorama", 
        "twine", 
        "setuptools", 
        "wheel"],
    entry_points={
        'console_scripts': ['pipcreator = pipcreator:cli'],
        },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)