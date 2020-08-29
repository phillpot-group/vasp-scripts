from vasp_scripts.outcar import Outcar


def test_outcar_get_total_energy():
    path = "./tests/data/OUTCAR"
    outcar = Outcar(path)
    outcar.read()
    target = -19.04159580
    res = outcar.get_total_energy()
    assert res == target


def test_outcar_get_total_cpu_time():
    path = "./tests/data/OUTCAR"
    outcar = Outcar(path)
    outcar.read()
    target = 186.747
    res = outcar.get_total_cpu_time()
    assert res == target
