"""Internal module with profiler stats class declaration."""

from pstats import Stats
from typing import Iterable, Mapping, Sequence


class ProfileStats(Stats):
    """A dummy override to explicitly describe class attributes.

    In the standard library, attributes are not defined in the constructor,
    which breaks the type analyzer.
    """

    __slots__ = (
        "all_callees",
        "files",
        "fcn_list",
        "total_tt",
        "total_calls",
        "prim_calls",
        "max_name_len",
        "top_level",
        "stats",
        "sort_arg_dict",
    )

    def __init__(self, *args, stream=None) -> None:
        """Initialize profile stats object."""
        self.all_callees = None
        self.files: Sequence = []
        self.fcn_list = None
        self.total_tt: int = 0
        self.total_calls: int = 0
        self.prim_calls: int = 0
        self.max_name_len: int = 0
        self.top_level: Iterable = set()
        self.stats: Mapping = {}
        self.sort_arg_dict: Mapping = {}

        super().__init__(*args, stream)
