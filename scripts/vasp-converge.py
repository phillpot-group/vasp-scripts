import argparse
import os
import shutil

import numpy as np

from pymatgen.io.vasp.inputs import Incar, Kpoints, Kpoints_supported_modes, Poscar

from rich.console import Console


def converge_kpoints(args, console):
    density_values = np.linspace(args.min, args.max, args.n)
    mode = Kpoints_supported_modes.from_string(args.mode)
    structure = Poscar.from_file("POSCAR").structure

    for i, density in enumerate(density_values):
        dirname = "kpoints-{}".format(i)
        console.print("[blue]{}:[/blue] density = {:.6E} /A^-1".format(density))
        os.mkdir(dirname)
        shutil.copy("INCAR", os.path.join(dirname, "INCAR"))
        shutil.copy("POSCAR", os.path.join(dirname, "POSCAR"))
        shutil.copy("POTCAR", os.path.join(dirname, "POTCAR"))
        shutil.copy(args.jobfile, os.path.join(dirname, args.jobfile))
        kpoints = Kpoints.automatic_density(structure, density)
        kpoints.style = mode
        kpoints.write_file(os.path.join(dirname, "KPOINTS"))
        os.chdir(dirname)
        os.system("{} {}".format(args.jobcmd, args.jobfile))
        os.chdir("..")


def converge_incar(args, console):
    for i, value in enumerate(args.values):
        dirname = "incar-{}".format(i)
        console.print("[blue]{}:[/blue] value = {}".format(value))
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
        os.system("{} {}".format(args.jobcmd, args.jobfile))
        os.chdir("..")


if __name__ == "__main__":
    console = Console()

    parser = argparse.ArgumentParser(description="Sets up convergence tests from input files in the current directory.")
    parser.add_argument("--jobcmd", default="sbatch", help="command used to submit a job file")
    parser.add_argument("--jobfile", default="runjob.slurm", help="filename of the job submission file")
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
    args.func(args, console)
    console.print("[bold green]SUCCESS:[/bold green] setup complete")
