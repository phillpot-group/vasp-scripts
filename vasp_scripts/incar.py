from typing import Dict, Optional

from vasp_scripts.util import TextFile


class Incar(TextFile):
    """VASP INCAR file parser."""

    def __init__(self, path: Optional[str] = None) -> None:
        if path is None:
            path = "INCAR"
        self._tags: Optional[Dict[str, str]] = None
        super().__init__(path)

    def read(self) -> None:
        super().read()
        self._tags = {}
        for line in self.lines:
            if line.startswith("#"):
                continue
            kv = line.split("=")
            if len(kv) != 2:
                continue
            key = kv[0].strip()
            value = kv[1].strip()
            value = value.split("#")[0].strip()
            self._tags[key] = value

    def write(self, path: Optional[str] = None) -> None:
        if path is None:
            path = self.path
        _lines = ["{} = {}".format(k, v) for k, v in self.tags.items()]
        with open(path, "w") as f:
            f.writelines(_lines)

    @property
    def tags(self) -> Dict[str, str]:
        if self._tags is None:
            raise RuntimeError("file not read")
        return self._tags
