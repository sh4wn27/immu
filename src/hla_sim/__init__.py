"""HLA equity simulation package."""

__version__ = "0.1.0"

SEED = 20260424  # global RNG seed; set via numpy.random.default_rng(SEED)

# Default populations to model — overridable per run.
DEFAULT_POPULATIONS = (
    "European (CEU)",
    "Han Chinese",
    "African American",
    "South Asian",
    "Middle Eastern",
    "Mexican American",
)

# HLA loci modeled. Extending to C / DQB1 is a documented future-work item.
LOCI = ("A", "B", "DRB1")
