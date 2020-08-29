from typing import Optional

from vasp_scripts.util import TextFile


class Outcar(TextFile):
    """VASP OUTCAR file parser."""

    def __init__(self, path: Optional[str] = None) -> None:
        if path is None:
            path = "OUTCAR"
        super().__init__(path)

    def get_total_energy(self) -> float:
        _lines = [line for line in self.lines if "TOTEN" in line]
        return float(_lines[-1].split()[-2])

    def get_total_cpu_time(self) -> float:
        _lines = [line for line in self.lines if line.startswith("Total CPU time used")]
        return float(_lines[-1].split()[-1])
