from copy import deepcopy
from typing import List, Tuple

from vedro.core import Dispatcher, Plugin, PluginConfig, ScenarioOrderer, VirtualScenario, ConfigType


class DependencyOrderer(ScenarioOrderer):
    def __init__(self, scenarios_paths):
        self._scenarios_paths = scenarios_paths

    async def sort(self, scenarios: List[VirtualScenario]) -> List[VirtualScenario]:
        all_indexes, diff_indexes = self._get_indexes_of_scenarios(scenarios, self._scenarios_paths)
        sequence_of_indexes = self._generate_sequence_of_indexes(all_indexes, diff_indexes)

        sorted_scenarios: List[VirtualScenario] = list()

        for index in sequence_of_indexes:
            sorted_scenarios.append(scenarios[index])

        return sorted_scenarios

    def _get_indexes_of_scenarios(self, scenarios: List[VirtualScenario], scenarios_paths: List[str]) -> Tuple:
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

    def _generate_sequence_of_indexes(self, all_indexes: List[int], diff_indexes: List[int]) -> List[int]:
        len_diff_indexes = len(diff_indexes)

        if all_indexes:
            len_all_indexes = len(all_indexes)
        else:
            all_indexes = deepcopy(diff_indexes)
            len_all_indexes = len_diff_indexes

        reversed_diff_indexes = deepcopy(diff_indexes)
        reversed_diff_indexes.reverse()

        sequence = list()
        boundary_position = len_all_indexes - 1

        for rev_index in reversed_diff_indexes:
            sequence.append(rev_index)
            boundary_position -= 1

            if boundary_position == 0:
                break

            for index in all_indexes[:boundary_position]:
                if index == rev_index:
                    continue
                sequence.append(index)
                sequence.append(rev_index)

        start_position = 0 if len_all_indexes == len_diff_indexes else len_all_indexes - len_diff_indexes - 1

        for index in all_indexes[start_position:]:
            sequence.append(index)

        return sequence
