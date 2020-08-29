from vasp_scripts.incar import Incar


def test_incar_tags():
    path = "./tests/data/INCAR"
    incar = Incar(path)
    incar.read()
    target = "31*5.0 32*0.6"
    res = incar.tags["MAGMOM"]
    assert res == target
