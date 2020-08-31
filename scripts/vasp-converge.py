import argparse
import os
import shutil

import numpy as np

from pymatgen.io.vasp.inputs import Incar, Kpoints, Kpoints_supported_modes, Poscar

from rich.console import Console
from rich.table import Table


def converge_kpoints(args, console):
    density_values = np.linspace(args.min, args.max, args.n)
    mode = Kpoints_supported_modes.from_string(args.mode)
    structure = Poscar.from_file("POSCAR").structure

    table = Table(title="K-point Convergence Summary")
    table.add_column("Directory")
    table.add_column("Density (atoms^-1)", justify="right")
    grids = []
    for density in density_values:
        kpoints = Kpoints.automatic_density(structure, density)
        kpoints.style = mode
        grid = (kpoints.kpts[0][0], kpoints.kpts[0][1], kpoints.kpts[0][2])
        if grid in grids:
            console.print("[bold yellow]WARNING:[/bold yellow] density {:.2f} does not produce a unique grid (skipping...)".format(density))
            continue
        grids.append(grid)
        dirname = "{}x{}x{}".format(grid[0], grid[1], grid[2])
        os.mkdir(dirname)
        shutil.copy("INCAR", os.path.join(dirname, "INCAR"))
        shutil.copy("POSCAR", os.path.join(dirname, "POSCAR"))
        shutil.copy("POTCAR", os.path.join(dirname, "POTCAR"))
        shutil.copy(args.jobfile, os.path.join(dirname, args.jobfile))
        kpoints.write_file(os.path.join(dirname, "KPOINTS"))
        os.chdir(dirname)
        #os.system("{} {}".format(args.jobcmd, args.jobfile))
        os.chdir("..")
        table.add_row(dirname, "{:.2f}".format(density))
    console.print(table)


def converge_incar(args, console):
    table = Table(title="{} Convergence Study".format(args.tag))
    table.add_column("Directory")
    table.add_column("{} Value".format(args.tag))
    for i, value in enumerate(args.values):
        dirname = "{}_{}".format(args.tag, i)
        os.mkdir(dirname)
        shutil.copy("POSCAR", os.path.join(dirname, "POSCAR"))
        shutil.copy("POTCAR", os.path.join(dirname, "POTCAR"))
        shutil.copy("KPOINTS", os.path.join(dirname, "KPOINTS"))
        shutil.copy(args.jobfile, os.path.join(dirname, args.jobfile))
        tags = Incar.from_file("INCAR").as_dict()
        tags[args.tag] = value
        incar = Incar.from_dict(tags)
        incar.write_file(os.path.join(dirname, "INCAR"))
        os.chdir(dirname)
        #os.system("{} {}".format(args.jobcmd, args.jobfile))
        os.chdir("..")
        table.add_row(dirname, "{}".format(value))
    console.print(table)


if __name__ == "__main__":
    console = Console()

    parser = argparse.ArgumentParser(description="Sets up convergence tests from input files in the current directory.")
    parser.add_argument("--jobcmd", default=os.environ.get("JOBCMD"), help="command used to submit a job file")
    parser.add_argument("--jobfile", default=os.environ.get("JOBFILE"), help="filename of the job submission file")
    subparsers = parser.add_subparsers()
    
    parser_kpoints = subparsers.add_parser("kpoints", help="signals k-point convergence")
    parser_kpoints.add_argument("min", type=float, help="minimum grid density")
    parser_kpoints.add_argument("max", type=float, help="maximum grid density")
    parser_kpoints.add_argument("n", type=int, help="number of density values to test")
    parser_kpoints.add_argument("--mode", default="gamma", help="grid construction mode")
    parser_kpoints.set_defaults(func=converge_kpoints)
    
    parser_incar = subparsers.add_parser("incar", help="signals INCAR tag convergence")
    parser_incar.add_argument("tag", help="name of the INCAR tag")
    parser_incar.add_argument("values", nargs="+", help="tag values to test")
    parser_incar.set_defaults(func=converge_incar)
    
    args = parser.parse_args()
    if args.jobcmd is None:
        args.jobcmd = "sbatch"
    if args.jobfile is None:
        args.jobfile = "runjob.slurm"
    args.func(args, console)
