import argparse
import os

import numpy as np

from pymatgen.io.vasp.inputs import Poscar
from pymatgen.io.vasp.outputs import Oszicar

from rich.console import Console
from rich.table import Table


def surface_defect(r_oszicar, d_oszicar, d_contcar, console):
    r_energy = r_oszicar.final_energy
    d_energy = d_oszicar.final_energy
    matrix = d_contcar.structure.lattice.matrix
    surface_area = np.linalg.norm(np.cross(matrix[0], matrix[1])) # xy plane
    res = (d_energy - r_energy) / (surface_area * 2.0)

    table = Table(title="Surface Formation Energy Results")
    table.add_column("Property", justify="left")
    table.add_column("Units", justify="center")
    table.add_column("Value", justify="center")
    table.add_row("Reference Total Energy", "eV", "{:.6E}".format(r_energy))
    table.add_row("Defective Total Energy", "eV", "{:.6e}".format(d_energy))
    table.add_row("Surface Area", "A^2", "{:.6E}".format(surface_area))
    table.add_row("Surface Formation Energy", "eV/A^2", "{:.6E}".format(res))
    console.print(table)


def point_defect(r_ozsicar, r_contcar, d_oszicar, d_contcar, console):
    r_energy = r_oszicar.final_energy
    d_energy = d_oszicar.final_energy
    r_structure = r_contcar.structure
    d_structure = d_contcar.structure
    r_energy_per_atom = r_energy / len(r_structure)
    res = d_energy - (r_energy_per_atom * len(d_structure))

    table = Table(title="Point Defect Formation Energy Results")
    table.add_column("Property", justify="left")
    table.add_column("Units", justify="center")
    table.add_column("Value", justify="center")
    table.add_row("Reference Total Energy", "eV", "{:.6E}".format(r_energy))
    table.add_row("Defective Total Energy", "eV", "{:.6e}".format(d_energy))
    table.add_row("Reference N Atoms", "atoms", "{}".format(len(r_structure)))
    table.add_row("Defective N Atoms", "atoms", "{}".format(len(d_structure)))
    table.add_row("Defect Formation Energy", "eV", "{:.6E}".format(res))
    console.print(table)


if __name__ == "__main__":
    console = Console()

    parser = argparse.ArgumentParser(description="Calculates the formation energy of various defect types.")
    parser.add_argument("type", help="type of defect to expect")
    parser.add_argument("reference", help="path to the reference system's calculation directory")
    parser.add_argument("defective", help="path to the defective system's calculation directory")
    args = parser.parse_args()

    r_oszicar = Oszicar(os.path.join(args.reference, "OSZICAR"))
    r_contcar = Poscar.from_file(os.path.join(args.reference, "CONTCAR"))
    d_oszicar = Oszicar(os.path.join(args.defective, "OSZICAR"))
    d_contcar = Poscar.from_file(os.path.join(args.defective, "CONTCAR"))

    if args.type == "surface":
        surface_defect(r_oszicar, d_oszicar, d_contcar, console)
    elif args.type == "point":
        point_defect(r_oszicar, r_contcar, d_oszicar, d_contcar, console)
    else:
        console.print("[bold red]ERROR:[/bold red] unsupported defect type '{}'".format(args.type))
