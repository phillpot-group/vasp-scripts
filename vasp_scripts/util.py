from typing import List, Optional


class TextFile(object):
    """Representation of a raw text file parser."""

    def __init__(self, path: str) -> None:
        self.path = path
        self._lines: Optional[List[str]] = None

    def read(self) -> None:
        with open(self.path, "r") as f:
            self._lines = [line.strip() for line in f.readlines()]

    def write(self, path: Optional[str] = None):
        if path is None:
            path = self.path
        with open(path, "w") as f:
            f.writelines(self.lines)

    @property
    def lines(self) -> List[str]:
        if self._lines is None:
            raise RuntimeError("file not read")
        return self._lines
