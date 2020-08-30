import argparse
import os
import shutil

import numpy as np

from pymatgen.io.vasp.inputs import Kpoints, Poscar

from rich.console import Console


if __name__ == "__main__":
    console = Console()

    parser = argparse.ArgumentParser(description="Run a k-points convergence study.")
    parser.add_argument("min", type=float, help="minimum k-point density")
    parser.add_argument("max", type=float, help="maximum k-point density")
    parser.add_argument("n", type=int, help="number of density values to test")
    parser.add_argument("--style", default="gamma")
    parser.add_argument("--jobcmd", default="sbatch")
    parser.add_argument("--jobfile", default="runjob.slurm")
    args = parser.parse_args()
    density_values = np.linspace(args.min, args.max, args.n)

    poscar = Poscar.from_file("POSCAR")
    structure = poscar.structure

    for density in density_values:
        kpoints = Kpoints.automatic_density(structure, density)
        dirname = "{:.6}".format(density)
        console.print("writing '{}'...".format(dirname))
        os.mkdir(dirname)
        shutil.copy("INCAR", os.path.join(dirname, "INCAR"))
        shutil.copy("POSCAR", os.path.join(dirname, "POSCAR"))
        shutil.copy("POTCAR", os.path.join(dirname, "POTCAR"))
        shutil.copy(args.jobfile, os.path.join(dirname, args.jobfile))
        kpoints.write_file(os.path.join(dirname, "KPOINTS"))

    console.print("setup complete.")
