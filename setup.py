from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="phillpot-vasp-scripts",
    version="0.1.2",
    description="A collection of scipts to automate common VASP tasks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Seaton Ullberg",
    author_email="sullberg@ufl.edu",
    url="https://github.com/phillpot-group/vasp-scripts",
    license="MIT License",
    scripts=[
        "scripts/vasp-compare.py",
        "scripts/vasp-converge.py",
        "scripts/vasp-defect-energy.py",
        "scripts/vasp-restart.py",
    ],
)
