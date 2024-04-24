from __future__ import annotations

from pathlib import Path

import serde.json


def read_source_json(infile: Path | str):
    return serde.json.deser(infile)
