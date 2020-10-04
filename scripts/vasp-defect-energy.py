import argparse
import os

import numpy as np

from pymatgen.io.vasp.inputs import Poscar
from pymatgen.io.vasp.outputs import Oszicar

from rich.console import Console
from rich.table import Table


def point_mode(args, console):
    perfect_contcar = Poscar.from_file(os.path.join(args.perfect, "CONTCAR"))
    perfect_oszicar = Oszicar(os.path.join(args.perfect, "OSZICAR"))
    defect_contcar = Poscar.from_file(os.path.join(args.defect, "CONTCAR"))
    defect_oszicar = Oszicar(os.path.join(args.defect, "OSZICAR"))
    ground_contcar = Poscar.from_file(os.path.join(args.ground, "CONTCAR"))
    ground_oszicar = Oszicar(os.path.join(args.ground, "OSZICAR"))

    perfect_energy = perfect_oszicar.final_energy
    perfect_natoms = len(perfect_contcar.structure)
    defect_energy = defect_oszicar.final_energy
    defect_natoms = len(defect_contcar.structure)
    ground_energy = ground_oszicar.final_energy
    ground_natoms = len(ground_contcar.structure)
    energy_per_atom = ground_energy / ground_natoms

    # negative for vacancy, positive for interstitial
    ndefects = defect_natoms - perfect_natoms
    
    res = defect_energy - perfect_energy - (ndefects * energy_per_atom)

    table = Table(title="Point Defect Formation Energy Results")
    table.add_column("Property", justify="left")
    table.add_column("Units", justify="center")
    table.add_column("Value", justify="center")
    table.add_row("Perfect System Total Energy", "eV", "{:.6E}".format(perfect_energy))
    table.add_row("Defective System Total Energy", "eV", "{:.6E}".format(defect_energy))
    table.add_row("Ground State Energy", "eV/atom", "{:.6E}".format(energy_per_atom))
    table.add_row("Perfect System N Atoms", "atoms", "{}".format(perfect_natoms))
    table.add_row("Perfect System N Atoms", "atoms", "{}".format(defect_natoms))
    table.add_row("Defect Formation Energy", "eV", "{:.6E}".format(res))
    console.print(table)


def surface_mode(args, console):
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

    table = Table(title="Surface Formation Energy Results")
    table.add_column("Property", justify="left")
    table.add_column("Units", justify="center")
    table.add_column("Value", justify="center")
    table.add_row("Perfect System Total Energy", "eV", "{:.6E}".format(perfect_energy))
    table.add_row("Defective System Total Energy", "eV", "{:.6e}".format(defect_energy))
    table.add_row("Surface Area", "A^2", "{:.6E}".format(area))
    table.add_row("Surface Formation Energy", "eV/A^2", "{:.6E}".format(res))
    console.print(table)


if __name__ == "__main__":
    console = Console()

    parser = argparse.ArgumentParser(description="Calculates the formation energy of various defect types.")
    subparsers = parser.add_subparsers()

    parser_point = subparsers.add_parser("point", help="signals point defect calculation")
    parser_point.add_argument("perfect", help="path to the perfect system's calculation directory")
    parser_point.add_argument("defect", help="path to the defective system's calculation directory")
    parser_point.add_argument("ground", help="path to the defect specie's ground state calculation directory")
    parser_point.set_defaults(func=point_mode)
    
    parser_surface = subparsers.add_parser("surface", help="signals surface formation energy calculation")
    parser_surface.add_argument("perfect", help="path to the perfect system's calculation directory")
    parser_surface.add_argument("defect", help="path to the defective system's calculation directory")
    parser_surface.add_argument("plane", default="xy", help="specifies which plane to interpret as surface ('xy', 'xz', or 'yz')")
    parser_surface.set_defaults(func=surface_mode)

    args = parser.parse_args()
    args.func(args, console)
