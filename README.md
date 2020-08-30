# vasp-scripts
Scripts to automate common operations with the Vienna Ab-initio Simulation Package.

## Installation

The collection can be downloaded from PyPI under the package name `phillpot-vasp-scripts`.

```bash
$ pip install phillpot-vasp-scripts
```

## Available Scripts

__[calculate-surface-energy.py](scripts/calculate-surface-energy.py)__ - Calculate surface formation energy from a bulk system and a system with an exposed surface. The two positional arguments should be the path to bulk and surface systems' calculation directories respectively.

![calculate-surface-energy.py](assets/calculate_surface_energy.png)