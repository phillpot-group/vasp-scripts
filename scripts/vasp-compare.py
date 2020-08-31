import argparse
import os

from pymatgen.io.vasp.outputs import Oszicar, Outcar

from rich.console import Console

from termgraph.termgraph import chart


def plot_energy(data, console):
    data = {k: v for k, v in sorted(data["energy"].items(), key=lambda item: item[1])}
    labels = list(data.keys())
    values = list(data.values())
    console.print("[bold]Final Energy[/bold]")
    _plot(labels, values, suffix=" eV", format="{:<5.6f}")


def plot_memory(data, console):
    data = {k: v for k, v in sorted(data["memory"].items(), key=lambda item: item[1])}
    labels = list(data.keys())
    values = list(data.values())
    console.print("[bold]Maximum Memory Usage[/bold]")
    _plot(labels, values, suffix=" kB", format="{:.0f}")


def plot_time(data, console):
    data = {k: v for k, v in sorted(data["time"].items(), key=lambda item: item[1])}
    labels = list(data.keys())
    values = list(data.values())
    console.print("[bold]Elapsed Time[/bold]")
    _plot(labels, values, suffix=" secs")


def _plot(labels, values, **kwargs):
    args = {
        "stacked": False,
        "width": 50,
        "no_labels": False,
        "format": "{:<5.2f}",
        "suffix": "",
        "vertical": False,
        "histogram": False,
        "no_values": False,
    }
    args.update(kwargs)
    data = [[x] for x in values]
    chart(colors=[], data=data, args=args, labels=labels)


if __name__ == "__main__":
    console = Console()
    parser = argparse.ArgumentParser(description="Compares the outputs of a series of calculations.")
    parser.add_argument("--ignore", nargs="*", help="directory names to remove from consideration")
    parser.add_argument("--energy", action="store_true", help="enables final energy comparison")
    parser.add_argument("--memory", action="store_true", help="enables memory usage comparison")
    parser.add_argument("--time", action="store_true", help="enables elapsed time comparison")
    args = parser.parse_args()
    if args.ignore is None:
        args.ignore = []

    data = {
        "energy": {},
        "memory": {},
        "time": {},
    }
    for dirname in os.listdir():
        if not os.path.isdir(dirname):
            continue
        if dirname in args.ignore:
            continue
        oszicar = Oszicar(os.path.join(dirname, "OSZICAR"))
        data["energy"][dirname] = oszicar.final_energy
        outcar = Outcar(os.path.join(dirname, "OUTCAR"))
        data["memory"][dirname] = outcar.run_stats["Maximum memory used (kb)"]
        data["time"][dirname] = outcar.run_stats["Elapsed time (sec)"]

    if args.energy:
        plot_energy(data, console)
    if args.memory:
        plot_memory(data, console)
    if args.time:
        plot_time(data, console)
