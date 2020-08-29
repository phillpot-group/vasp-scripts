from typing import Optional, Tuple

from vasp_scripts.util import TextFile


class Kpoints(TextFile):
    """VASP KPOINTS file parser."""

    def __init__(self, path: Optional[str] = None) -> None:
        if path is None:
            path = "KPOINTS"
        self._grid_size: Optional[Tuple[int, int, int]] = None
        self._grid_style: Optional[str] = None
        super().__init__(path)

    def read(self) -> None:
        super().read()
        self._grid_style = self.lines[2]
        _grid_size = self.lines[3].split()
        self._grid_size = (
            int(_grid_size[0]),
            int(_grid_size[1]),
            int(_grid_size[2]),
        )

    @property
    def grid_size(self) -> Tuple[int, int, int]:
        if self._grid_size is None:
            raise RuntimeError("file not read")
        return self._grid_size

    @grid_size.setter
    def grid_size(self, value: Tuple[int, int, int]) -> None:
        self._grid_size = value

    @property
    def grid_style(self) -> str:
        if self._grid_style is None:
            raise RuntimeError("file not read")
        return self._grid_style

    @grid_style.setter
    def grid_style(self, value: str) -> None:
        self._grid_style = value
