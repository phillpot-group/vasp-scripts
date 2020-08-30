import argparse
import os

from pymatgen.io.vasp.outputs import Oszicar, Outcar

from termgraph.termgraph import chart


def plot_energy(data):
    labels = list(data)
    values = [data[k]["energy"] for k in data]
    _plot(labels, values, title="Final Energy (eV)")


def plot_memory(data):
    labels = list(data)
    values = [data[k]["memory"] for k in data]
    _plot(labels, values, title="Average Memory Usage (kB)")


def plot_time(data):
    labels = list(data)
    values = [data[k]["time"] for k in data]
    _plot(labels, values, title="Elapsed Time (sec)")


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
    parser = argparse.ArgumentParser(description="Compares the outputs of a series of calculations.")
    parser.add_argument("--ignore", nargs="*", help="directory names to remove from consideration")
    parser.add_argument("--energy", action="store_true", help="enables final energy comparison")
    parser.add_argument("--memory", action="store_true", help="enables memory usage comparison")
    parser.add_argument("--time", action="store_true", help="enables elapsed time comparison")
    args = parser.parse_args()
    if args.ignore is None:
        args.ignore = []

    data = {}
    for dirname in os.listdir():
        if not os.path.isdir(dirname):
            continue
        if dirname in args.ignore:
            continue
        data[dirname] = {}

        oszicar = Oszicar(os.path.join(dirname, "OSZICAR"))
        data[dirname]["energy"] = oszicar.final_energy
        outcar = Outcar(os.path.join(dirname, "OUTCAR"))
        data[dirname]["memory"] = outcar.run_stats["Average memory used (kb)"]
        data[dirname]["time"] = outcar.run_stats["Elapsed time (sec)"]

    if args.energy:
        plot_energy(data)
    if args.memory:
        plot_memory(data)
    if args.time:
        plot_time(data)
