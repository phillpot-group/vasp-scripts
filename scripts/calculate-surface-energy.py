import argparse
import os

import numpy as np

from pymatgen.io.vasp.inputs import Poscar
from pymatgen.io.vasp.outputs import Oszicar

from rich.console import Console


parser = argparse.ArgumentParser(description="Calculate surface energy.")
parser.add_argument("bulk", help="path to the bulk reference calculation")
parser.add_argument("surface", help="path to the surface structure calculation")
args = parser.parse_args()

oszicar = Oszicar(os.path.join(parser.bulk, "OSZICAR"))
bulk_final_energy = oszicar.final_energy

oszicar = Oszicar(os.path.join(parser.surface, "OSZICAR"))
surface_final_energy = oszicar.final_energy
contcar = Poscar().from_file(os.path.join(parser.surface, "CONTCAR"))
matrix = contcar.structure.lattice.matrix
# area of the xy plane
surface_area = np.linalg.norm(np.cross(matrix[0], matrix[1]))
res = (surface_final_energy - bulk_final_energy) / surface_area

console = Console()
console.print("Surface Energy (eV/A^2): {}".format(res))
