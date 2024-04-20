# -*- coding: utf-8 -*-

"""Download registry information from CROPOCT."""

import io
import json
import logging
from pathlib import Path

import yaml
from pystow.utils import download

from bioregistry.constants import RAW_DIRECTORY
from bioregistry.external.alignment_utils import Aligner

__all__ = [
    "get_cropoct",
    "CropOCTAligner",
]

logger = logging.getLogger(__name__)

DIRECTORY = Path(__file__).parent.resolve()
RAW_PATH = RAW_DIRECTORY / "cropoct.yaml"
PROCESSED_PATH = DIRECTORY / "processed.json"
CROPOCT_URL = "https://cropontology.org/metadata"


def get_cropoct(force_download: bool = False):
    """Get the CropOCT registry."""
    if PROCESSED_PATH.exists() and not force_download:
        with PROCESSED_PATH.open() as file:
            return json.load(file)

    download(url=CROPOCT_URL, path=RAW_PATH, force=True)

    lines = []
    with RAW_PATH.open() as file:
        next(file)  # throw away header
        for i, line in enumerate(file):
            line = line.rstrip()
            line = line.replace(" : ", ": ")
            if line.count('"') > 2:
                logger.debug("issue on line %s: %s", i, line)
                continue
            lines.append(line)

    fixed = "\n".join(lines)
    RAW_PATH.write_text(
        yaml.safe_dump(
            yaml.safe_load(io.StringIO(fixed)),
            indent=2,
        )
    )
    with RAW_PATH.open() as file:
        data = yaml.safe_load(file)

    rv = {record["id"]: _process(record) for record in data["ontologies"]}
    with PROCESSED_PATH.open("w") as file:
        json.dump(rv, file, indent=2, sort_keys=True)
    return rv


def _process(record):
    rv = {
        "prefix": record["id"],
        "name": record["title"],
        "homepage": record["homepage"],
        "download_owl": record.get("ontology_purl"),
        "description": record.get("description"),
    }
    return {k: v for k, v in rv.items() if k and v}


class CropOCTAligner(Aligner):
    """Aligner for CropOCT."""

    key = "cropoct"
    getter = get_cropoct
    curation_header = ["name", "homepage", "description"]


if __name__ == "__main__":
    CropOCTAligner.cli()
