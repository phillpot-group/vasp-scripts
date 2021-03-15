import argparse

from pymatgen.io.vasp.outputs import Vasprun

from rich.console import Console
from rich.table import Table


def extract_band_gap(console, table):
    try:
        vasprun = Vasprun("vasprun.xml")
    except:
        console.print("Unable to locate vasprun.xml")
        exit()

    band_gap, cbm, vbm, _ = vasprun.eigenvalue_band_properties
    fmt = "{:.4f}"
    table.add_row("Band Gap", fmt.format(band_gap), "eV")
    table.add_row("Conduction Band Minimum", fmt.format(cbm), "eV")
    table.add_row("Valence Band Maximum", fmt.format(vbm), "eV")


if __name__ == "__main__":
    console = Console()

    parser = argparse.ArgumentParser(description="Extracts a property from output files in the current directory.")
    parser.add_argument(
        "--band-gap",
        help="extracts the band gap from a vasprun.xml file",
        action="store_true",
        dest="band_gap",
    )

    table = Table(title="Simulation Properties")
    table.add_column("Name")
    table.add_column("Value")
    table.add_column("Units")

    args = parser.parse_args()
    if args.band_gap:
        extract_band_gap(console, table)
    else:
        console.print("No properties selected")
        exit()

    console.print(table)

