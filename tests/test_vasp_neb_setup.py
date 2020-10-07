import os
import shutil

import pytest


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture
def setup(tmpdir):
    # generate paths to test data
    data_paths = {
        "initial": {
            "CONTCAR": os.path.join(DATA_DIR, "MnCr2O4.16C-32E.initial.poscar"),
            "OUTCAR": os.path.join(DATA_DIR, "MnCr2O4.16C-32E.initial.outcar"),
        },
        "final": {
            "CONTCAR": os.path.join(DATA_DIR, "MnCr2O4.16C-32E.final.poscar"),
            "OUTCAR": os.path.join(DATA_DIR, "MnCr2O4.16C-32E.final.outcar"),
        }
    }

    # generate temporary test directories and files
    for dirname in ["initial", "final"]:
        _tmpdir = tmpdir.mkdir(dirname)
        for filename in ["CONTCAR", "OUTCAR"]:
            shutil.copy(
                data_paths[dirname][filename],
                _tmpdir.join(filename)
            )

    return {"data_paths": data_paths, "tmpdir": tmpdir}


def test_custom_interpolator(setup, script_runner):
    # load setup resources
    data_paths = setup["data_paths"]
    tmpdir = setup["tmpdir"]

    # generate neb.positions file
    tmpdir.join("neb.positions").write("0.0 0.0 0.0\n0.25 0.25 0.25")

    # execute the script
    os.chdir(tmpdir)
    res = script_runner.run(
        "vasp-neb-setup.py", 
        str(tmpdir.join("initial")), 
        str(tmpdir.join("final")), 
        "5"
    )

    # validate results
    assert res.success
    assert len(os.listdir(tmpdir)) == 11


def test_pymatgen_interpolator(setup, script_runner):
    # load setup resources
    data_paths = setup["data_paths"]
    tmpdir = setup["tmpdir"]

    # execute the script
    os.chdir(tmpdir)
    res = script_runner.run(
        "vasp-neb-setup.py", 
        str(tmpdir.join("initial")), 
        str(tmpdir.join("final")), 
        "5"
    )

    # validate results
    assert res.success
    print(os.listdir(tmpdir))
    assert len(os.listdir(tmpdir)) == 10