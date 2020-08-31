import argparse
import os

from pymatgen.io.vasp.inputs import Incar

from rich.console import console


if __name__ == "__main__":
    console = Console()

    parser = argparse.ArgumentParser(description="Restarts a calculation after timeout or failure.")
    parser.add_argument("--jobcmd", default=os.environ.get("JOBCMD"), help="command used to submit a job file")
    parser.add_argument("--jobfile", default=os.environ.get("JOBFILE"), help="filename of the job submission file")
    args = parser.parse_args()
    if args.jobcmd is None:
        args.jobcmd = "sbatch"
    if args.jobfile is None:
        args.jobfile = "runjob.slurm"

    os.remove("POSCAR")
    os.rename("CONTCAR", "POSCAR")
    incar = Incar.from_file("INCAR")
    incar_tags = incar.as_dict()
    incar_tags["ISTART"] = 1
    incar = Incar.from_dict(incar_tags)
    incar.write_file("INCAR")
    os.system("{} {}".format(args.jobcmd, args.jobfile))

    console.print("[bold green]SUCCESS:[/bold green] job restarted")
