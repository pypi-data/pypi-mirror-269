from __future__ import annotations
from typing import Any, Optional, Iterator

from kojo.item import Item


class TabularReader:
    """A generator to provide kojo.Items from tabular data"""

    iterator: Iterator[list[Any]]
    headers: list[str]
    index: int
    default_cell_value: Any

    def __init__(
        self,
        inner_iterator: Iterator[list[Any]],
        default_cell_value: Optional[Any] = None,
    ) -> None:
        self.iterator = inner_iterator
        self.default_cell_value = default_cell_value
        self.headers = [str(h) for h in next(self.iterator)]
        self.index = 0

    def __next__(self) -> Item:
        row = next(self.iterator)
        lr = len(row)
        lh = len(self.headers)
        if lr < lh:
            # fill missing rows with default value
            for _ in range(lr, lh):
                row.append(self.default_cell_value)
        item = Item({self.headers[i]: cell for (i, cell) in enumerate(row)})

        item.meta["index"] = self.index
        self.index += 1

        return item

    def __iter__(self) -> TabularReader:
        return self
