import argparse
import copy
import os
import shutil

import numpy as np

from pymatgen.io.vasp.inputs import Poscar
from pymatgen.io.vasp.outputs import Outcar

from rich.console import Console
from rich.table import Table


NEB_POSITIONS_FNAME = "neb.positions"


def neb_setup(args, console):
    initial_contcar = Poscar.from_file(os.path.join(args.initial, "CONTCAR"))
    final_contcar = Poscar.from_file(os.path.join(args.final, "CONTCAR"))

    positions = None
    if os.path.exists(NEB_POSITIONS_FNAME):
        positions = np.loadtxt(NEB_POSITIONS_FNAME)
    
    images = []
    if positions is None:
        # call pymatgen interpolator
        images = initial_contcar.structure.interpolate(final_contcar.structure, nimages=args.nimages)        
    else:
        # call custom interpolator
        images = custom_interpolate(
            initial_contcar.structure, 
            final_contcar.structure, 
            args.nimages, 
            positions
        )

    for i, image in enumerate(images):
        dirname = f"{i:02}"
        os.mkdir(dirname)
        with open(os.path.join(dirname, "POSCAR")) as f:
            f.write(Poscar(image).get_string())

    # copy OUTCARs for post-processing
    shutil.copy(
        os.path.join(args.initial, "OUTCAR"), 
        os.path.join("00", "OUTCAR")
    )
    shutil.copy(
        os.path.join(args.final, "OUTCAR"), 
        os.path.join(dirname, "OUTCAR")
    )


def custom_interpolate(initial, final, nimages, positions):
    # initialize intermediate images
    images = [copy.deepcopy(initial) for _ in range(nimages)]
    
    # iterate over the initial/final pairs
    for i in enumerate(positions):
        # skip finals and break at end
        if i % 2 != 0:
            if i == len(positions - 1):
                break
            else:
                continue

        # parse pair into initial and final
        initial_pos = positions[i]
        final_pos = positions[i+1]

        # check that the initial site is occupied
        initial_sites = initial.get_sites_in_sphere(initial_pos, 1.0E-6, include_index=True)
        if len(initial_sites) == 0:
            # TODO: log error
            raise RuntimeError
        initial_index = initial_sites[0][2]
        initial_specie = initial_sites[0][0].specie

        # check that the final site is unoccupied
        if len(final.get_sites_in_sphere(final_pos, 1.0E-6)) != 0:
            # TODO: log error
            raise RuntimeError

        # calculate path between final and initial
        diff = final_pos - initial_pos
        step = diff / nimages

        # interpolate points along the path
        points = [initial_pos + (step * (i+1)) for i in range(nimages)]

        # remove the initial site
        images[0].remove_sites([initial_index])
        # insert the interpolated sites
        for j, point in enumerate(points):
            images[j].insert(initial_index, initial_specie, point)

    return images


if __name__ == "__main__":
    console = Console()

    parser = argparse.ArgumentParser(description="Generates intermediate images for NEB calculations.")
    parser.add_argument("initial", help="path to the initial system's calculation directory")
    parser.add_argument("final", help="path to the final system's calculation directory")
    parser.add_argument("nimages", type=int, help="number of intermediate images to produce")
    parser.set_defaults(func=neb_setup)

    args = parser.parse_args()
    args.func(args, console)
