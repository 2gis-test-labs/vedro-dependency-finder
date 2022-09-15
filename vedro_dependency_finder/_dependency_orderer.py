from typing import List, Tuple

from ._generate_sequence_of_indexes import generate_sequence_of_indexes
from vedro.core import ScenarioOrderer, VirtualScenario


class DependencyOrderer(ScenarioOrderer):
    def __init__(self, scenarios_paths: List[str]):
        self._scenarios_paths = scenarios_paths

    async def sort(self, scenarios: List[VirtualScenario]) -> List[VirtualScenario]:
        all_indexes, diff_indexes = self._get_indexes_of_scenarios(
            scenarios, self._scenarios_paths
        )
        sequence_of_indexes = generate_sequence_of_indexes(all_indexes, diff_indexes)
        sorted_scenarios = list()

        for index in sequence_of_indexes:
            sorted_scenarios.append(scenarios[index])

        return sorted_scenarios

    def _get_indexes_of_scenarios(self, scenarios: List[VirtualScenario],
                                  scenarios_paths: List[str]) -> Tuple[List[int], List[int]]:
        all_indexes = list(range(len(scenarios)))
        diff_indexes = list()

        for scenario in scenarios:
            if str(scenario.rel_path) in scenarios_paths:
                diff_indexes.append(scenarios.index(scenario))

        # перемещаем diff_index'ы в конец all_indexes,
        # для правильной генерации последовательности
        for diff_index in diff_indexes:
            if diff_index in all_indexes:
                all_indexes += [all_indexes.pop(diff_index)]

        return all_indexes, diff_indexes
