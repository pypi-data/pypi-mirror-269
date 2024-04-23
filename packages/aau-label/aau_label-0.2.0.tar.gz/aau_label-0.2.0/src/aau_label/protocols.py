from pathlib import Path
from typing import ClassVar, Protocol, Sequence

from PIL.Image import Image


class Label(Protocol):
    x: int
    y: int
    width: int
    height: int
    name: str


class LabelImage(Protocol):
    path: Path
    width: int
    height: int
    labels: Sequence[Label]


class LabelParser(Protocol):
    file_extension: ClassVar[str]

    def parse(self, label_file: Path, image: Image) -> Sequence[Label]:
        raise NotImplementedError
