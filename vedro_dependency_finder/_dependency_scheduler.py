from vedro.core import (
    VirtualScenario,
    AggregatedResult,
    ScenarioResult,
    MonotonicScenarioScheduler,
    ScenarioScheduler,
)
from typing import List, Iterator, Tuple


class DependencyScheduler(MonotonicScenarioScheduler):
    def __init__(self, scenarios: List[VirtualScenario]) -> None:
        super().__init__(scenarios)
        self._discovered = [(scn.unique_id, scn) for scn in scenarios]
        self._scheduled = [(k, (v, 0)) for k, v in reversed(self._discovered)]
        self._queue: List[str, Tuple[VirtualScenario, int]] = list()

    @property
    def discovered(self) -> Iterator[VirtualScenario]:
        for item in self._discovered:
            yield item[1]

    @property
    def scheduled(self) -> Iterator[VirtualScenario]:
        for item in reversed(self._scheduled):
            scenario, repeats = self._scheduled[item[0]]
            for _ in range(repeats + 1):
                yield scenario

    def ignore(self, scenario: VirtualScenario) -> None:
        self._scheduled.pop(scenario.unique_id)
        self._queue.pop(scenario.unique_id)

    async def __anext__(self) -> VirtualScenario:
        while len(self._queue) > 0:
            _, (scenario, repeats) = self._queue.pop()
            if repeats > 0:
                self._queue[scenario.unique_id] = (scenario, repeats - 1)
            return scenario
        raise StopAsyncIteration()
