import argparse
import os

import numpy as np

from pymatgen.io.vasp.inputs import Poscar
from pymatgen.io.vasp.outputs import Oszicar

from rich.console import Console
from rich.table import Table


def surface_energy(args, console, table):
    perfect_oszicar = Oszicar(os.path.join(args.perfect, "OSZICAR"))
    defect_oszicar = Oszicar(os.path.join(args.defect, "OSZICAR"))
    defect_contcar = Poscar.from_file(os.path.join(args.defect, "CONTCAR"))

    matrix = defect_contcar.structure.lattice.matrix
    calc_area = lambda i, j: np.linalg.norm(np.cross(matrix[i], matrix[j]))
    if args.plane == "xy":
        area = calc_area(0, 1)
    elif args.plane == "xz":
        area = calc_area(0, 2)
    elif args.plane == "yz":
        area = calc_area(1, 2)
    else:
        console.print("[bold red]ERROR:[/bold red] invalid option for argument `plane`")
        exit()

    defect_energy = defect_oszicar.final_energy
    perfect_energy = perfect_oszicar.final_energy
    res = (defect_energy - perfect_energy) / (area * 2.0)

    fmt = "{:.4f}"
    table.add_row("Perfect System Total Energy", fmt.format(perfect_energy), "eV")
    table.add_row("Defective System Total Energy", fmt.format(defect_energy), "eV")
    table.add_row("Surface Area", fmt.format(area), "A^2")
    table.add_row("Surface Formation Energy", fmt.format(res), "eV/A^2")


if __name__ == "__main__":
    console = Console()

    parser = argparse.ArgumentParser(description="Calculates surface formation energy.")
    parser.add_argument("perfect", help="path to the perfect system's calculation directory")
    parser.add_argument("defect", help="path to the defective system's calculation directory")
    parser.add_argument("plane", default="xy", help="specifies which plane to interpret as a surface ('xy', 'xz', or 'yz')")
    parser.set_defaults(func=surface_energy)

    table = Table(title="Surface Formation Energy Summary")
    table.add_column("Property")
    table.add_column("Value")
    table.add_column("Units")

    args = parser.parse_args()
    args.func(args, console, table)

    console.print(table)

