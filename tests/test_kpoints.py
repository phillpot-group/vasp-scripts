from vasp_scripts.kpoints import Kpoints


def test_kpoints_grid_size():
    path = "./tests/data/KPOINTS"
    kpoints = Kpoints(path)
    kpoints.read()
    target = (3, 3, 3)
    res = kpoints.grid_size
    assert res == target


def test_kpoints_grid_style():
    path = "./tests/data/KPOINTS"
    kpoints = Kpoints(path)
    kpoints.read()
    target = "Gamma"
    res = kpoints.grid_style
    assert res == target
