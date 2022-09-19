from typing import List, Tuple

from vedro.core import VirtualScenario


def get_indexes_of_scenarios(scenarios: List[VirtualScenario],
                             scenarios_paths: List[str]) -> Tuple[List[int], List[int]]:
    assert scenarios, "Scenarios not found!"
    assert scenarios_paths, "Paths of scenarios not found!"

    all_indexes = list(range(len(scenarios)))
    diff_indexes = list()

    for scenario in scenarios:
        if str(scenario.rel_path) in scenarios_paths:
            diff_indexes.append(scenarios.index(scenario))

    assert diff_indexes, "The selected scripts are not contained in the selected tests folder!"

    # перемещаем diff_index'ы в конец all_indexes,
    # для правильной генерации последовательности
    for diff_index in diff_indexes:
        if diff_index in all_indexes:
            all_indexes += [all_indexes.pop(all_indexes.index(diff_index))]

    return all_indexes, diff_indexes
