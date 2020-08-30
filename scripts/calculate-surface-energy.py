import argparse
import os

import numpy as np

from pymatgen.io.vasp.inputs import Poscar
from pymatgen.io.vasp.outputs import Oszicar

from rich.console import Console
from rich.table import Table


if __name__ == "__main__":
    console = Console()
    
    parser = argparse.ArgumentParser(description="Calculate surface energy.")
    parser.add_argument("bulk", help="path to the bulk reference calculation")
    parser.add_argument("surface", help="path to the surface structure calculation")
    args = parser.parse_args()

    oszicar = Oszicar(os.path.join(args.bulk, "OSZICAR"))
    bulk_final_energy = oszicar.final_energy

    oszicar = Oszicar(os.path.join(args.surface, "OSZICAR"))
    surface_final_energy = oszicar.final_energy
    contcar = Poscar.from_file(os.path.join(args.surface, "CONTCAR"))
    matrix = contcar.structure.lattice.matrix
    # area of the xy plane
    surface_area = np.linalg.norm(np.cross(matrix[0], matrix[1]))
    res = (surface_final_energy - bulk_final_energy) / (surface_area * 2.0)

    table = Table(title="Surface Energy Results")
    table.add_column("Property", justify="left")
    table.add_column("Units", justify="center")
    table.add_column("Value", justify="center", no_wrap=True)
    table.add_row("Bulk Total Energy", "eV", "{:.6E}".format(bulk_final_energy))
    table.add_row("Surface Total Energy", "eV", "{:.6e}".format(surface_final_energy))
    table.add_row("Surface Area", "A^2", "{:.6E}".format(surface_area))
    table.add_row("Surface Formation Energy", "eV/A^2", "{:.6E}".format(res))

    console.print(table)
