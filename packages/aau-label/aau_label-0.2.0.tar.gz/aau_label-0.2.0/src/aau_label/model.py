from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .protocols import Label


@dataclass
class AAULabel:
    x: int
    y: int
    width: int
    height: int
    name: str


@dataclass
class AAULabelImage:
    path: Path
    width: int
    height: int
    labels: Sequence[Label]
    source: str | None = None


@dataclass
class COCOLicense:
    name: str
    url: str


@dataclass
class COCOInfo:
    year: int
    version: str
    description: str
    contributor: str
    url: str
    date_created: str
