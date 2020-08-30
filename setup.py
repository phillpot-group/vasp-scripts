from setuptools import setup


setup(
    name="phillpot-vasp-scripts",
    version="0.1.0",
    description="A collection of scipts to automate common VASP tasks.",
    author="Seaton Ullberg",
    author_email="sullberg@ufl.edu",
    url="https://github.com/phillpot-group/vasp-scripts",
    license="MIT License",
    scripts=[
        "scripts/vasp-converge.py",
        "scripts/vasp-defect-energy.py",
    ],
    install_requires=[
        "pymatgen", 
        "rich", 
        "termgraph"
    ],
)
