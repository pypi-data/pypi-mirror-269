from __future__ import annotations
import json
from typing import Any, Callable, Iterable, Iterator

from kojo.item import Item


def apply(iterable: Iterable[Item], *processes: Process) -> Iterator[Item]:
    for item in iterable:
        processed_item = apply_on_item(item, *processes)
        if processed_item is not None:
            yield processed_item


def apply_on_item(item: Item | None, *processes: Process) -> Item | None:
    for process in processes:
        for step in process.steps:
            if item is None:
                return None
            item = step(item)
    return item


MapStepFunction = Callable[[Item], Item]
FilterStepFunction = Callable[[Item], bool]


class MapStep:
    fn: MapStepFunction

    def __init__(self, fn: MapStepFunction):
        self.fn = fn

    def __call__(self, item: Item) -> Item:
        return self.fn(item)


class FilterStep:
    fn: FilterStepFunction

    def __init__(self, fn: FilterStepFunction):
        self.fn = fn

    def __call__(self, item: Item) -> Item | None:
        keep = self.fn(item)
        return item if keep else None


class Process:
    steps: list[FilterStep | MapStep]

    def __init__(self) -> None:
        self.steps = []

    def map(self, fn: MapStepFunction) -> Process:
        self.steps.append(MapStep(fn))
        return self

    def filter(self, fn: FilterStepFunction) -> Process:
        self.steps.append(FilterStep(fn))
        return self

    def __call__(self, iterable: Iterable[Item]) -> Iterator[Item]:
        return apply(iterable, self)

    def __iadd__(self, fn: MapStepFunction) -> Process:
        return self.map(fn)

    def __imul__(self, fn: FilterStepFunction) -> Process:
        return self.filter(fn)


class StepEncoder(json.JSONEncoder):
    def default(self, step: FilterStep | MapStep) -> dict[str, Any]:
        obj = {
            "type": step.__class__.__name__,
            "module": step.fn.__module__,
            "name": step.fn.__name__,
            "description": step.fn.__doc__,
        }
        return obj


class ProcessEncoder(json.JSONEncoder):
    def default(self, process: Process) -> list[dict[str, Any]]:
        child_encoder = StepEncoder()
        return [child_encoder.default(step) for step in process.steps]
