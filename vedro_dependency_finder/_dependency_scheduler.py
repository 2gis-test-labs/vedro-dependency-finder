from typing import List

from vedro.core import MonotonicScenarioScheduler, VirtualScenario

from ._generate_sequence_of_indexes import generate_sequence_of_indexes
from ._get_indexes_of_scenarios import get_indexes_of_scenarios


class DependencyScheduler(MonotonicScenarioScheduler):
    def __init__(self, scenarios: List[VirtualScenario], diff_scenarios_paths: List[str]) -> None:
        super().__init__(scenarios)
        self._diff_scenarios_paths = diff_scenarios_paths

    def __aiter__(self) -> "DependencyScheduler":
        scenarios = [scn for scn, _ in self._scheduled.values()]
        all_indexes, diff_indexes = get_indexes_of_scenarios(
            scenarios, self._diff_scenarios_paths
        )
        sequence_of_indexes = generate_sequence_of_indexes(all_indexes, diff_indexes)
        self._scenarios = list()

        for index in sequence_of_indexes:
            self._scenarios.append(scenarios[index])
        return super().__aiter__()

    async def __anext__(self) -> VirtualScenario:
        while len(self._scenarios) > 0:
            return self._scenarios.pop()
        raise StopAsyncIteration()
