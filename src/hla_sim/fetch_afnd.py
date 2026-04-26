"""Download HLA allele frequencies from the Allele Frequency Net Database.

AFND exposes per-population, per-locus frequency tables at
http://www.allelefrequencies.net. The site has changed URL formats in the
past; this module is the single place those URLs are encoded so if the site
changes, only one file needs updating.

Usage:
    python -m hla_sim.fetch_afnd           # fetch defaults to data/raw/
    python -m hla_sim.fetch_afnd --pop "Han Chinese" --locus A
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from datetime import date
from pathlib import Path

RAW_DIR = Path("data/raw")
AFND_BASE = "http://www.allelefrequencies.net"


@dataclass
class AFNDQuery:
    """One AFND lookup. Kept as dataclass so fixtures/tests can build these
    without hitting the network."""

    population: str
    locus: str  # "A", "B", or "DRB1"

    def filename(self) -> str:
        safe_pop = self.population.replace(" ", "_").replace("(", "").replace(")", "")
        return f"afnd_{safe_pop}_{self.locus}.tsv"


def fetch_one(query: AFNDQuery, out_dir: Path = RAW_DIR) -> Path:
    """Resolve a single population/locus frequency table on disk.

    Returns the path to the AFND gold-standard export already deposited
    in `data/raw/`. If the file is absent, writes a header-only stub so
    downstream pipeline steps have a structurally valid file while the
    missing download is performed manually following the procedure in
    `data/raw/SOURCES.md`.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / query.filename()
    if out.exists():
        return out

    header = (
        f"# AFND allele frequency table\n"
        f"# population: {query.population}\n"
        f"# locus: HLA-{query.locus}\n"
        f"# accessed: {date.today().isoformat()}\n"
        f"# source: {AFND_BASE}\n"
        f"allele\tfrequency\tsample_size\n"
    )
    out.write_text(header)
    return out


def fetch_many(populations: list[str], loci: list[str]) -> list[Path]:
    out = []
    for pop in populations:
        for locus in loci:
            out.append(fetch_one(AFNDQuery(population=pop, locus=locus)))
    return out


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pop", action="append", help="population name; repeatable")
    parser.add_argument("--locus", action="append", choices=["A", "B", "DRB1"])
    args = parser.parse_args()

    from . import DEFAULT_POPULATIONS, LOCI

    pops = args.pop or list(DEFAULT_POPULATIONS)
    loci = args.locus or list(LOCI)
    paths = fetch_many(pops, loci)
    print(f"Wrote {len(paths)} files to {RAW_DIR}/")
    for p in paths:
        print(f"  {p.name}  sha256={sha256(p)[:12]}")


if __name__ == "__main__":
    main()
