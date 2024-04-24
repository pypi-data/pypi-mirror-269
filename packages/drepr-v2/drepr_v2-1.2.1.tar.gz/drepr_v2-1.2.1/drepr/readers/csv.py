from __future__ import annotations

from pathlib import Path

import serde.csv


def read_source_csv(infile: Path | str):
    return serde.csv.deser(infile)
