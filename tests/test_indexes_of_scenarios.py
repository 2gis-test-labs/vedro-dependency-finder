from pathlib import Path
from typing import List
from unittest.mock import Mock

import pytest
from baby_steps import given, then, when
from pytest import raises
from vedro import Scenario
from vedro.core import VirtualScenario

from vedro_dependency_finder._get_indexes_of_scenarios import get_indexes_of_scenarios


def create_scenario(filename):
    return Mock(Scenario, __file__=filename)


def test_indexes_of_all_scenarios():
    with given:
        scenarios = list()
        scenarios_paths = list()

        iterator = range(0, 3)

        root = Path("/tmp/app")

        for i in iterator:
            path = f"scenario_{i}.py"
            scenarios_paths.append(path)
            scn = create_scenario(root / path)
            scenarios.append(VirtualScenario(scn, []))

    with when:
        all_indexes, diff_indexes = get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert all_indexes == list(iterator)
        assert diff_indexes == list(iterator)


def test_diff_indexes_at_the_beginning_of_all_indexes():
    with given:
        scenarios = list()
        scenarios_paths = list()

        iterator = range(0, 5)
        diff_list = list(range(0, 3))

        root = Path("/tmp/app")

        for i in iterator:
            path = f"scenario_{i}.py"
            scn = create_scenario(root / path)
            scenarios.append(VirtualScenario(scn, []))

            if i in diff_list:
                scenarios_paths.append(f"scenario_{i}.py")

    with when:
        all_indexes, diff_indexes = get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert all_indexes == [3, 4, 0, 1, 2]
        assert diff_indexes == diff_list


def test_diff_indexes_in_the_middle_of_all_indexes():
    with given:
        scenarios = list()
        scenarios_paths = list()

        iterator = range(0, 5)
        diff_list = list(range(2, 4))

        root = Path("/tmp/app")

        for i in iterator:
            path = f"scenario_{i}.py"
            scn = create_scenario(root / path)
            scenarios.append(VirtualScenario(scn, []))

            if i in diff_list:
                scenarios_paths.append(f"scenario_{i}.py")

    with when:
        all_indexes, diff_indexes = get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert all_indexes == [0, 1, 4, 2, 3]
        assert diff_indexes == diff_list


def test_diff_indexes_at_the_end_of_all_indexes():
    with given:
        scenarios = list()
        scenarios_paths = list()

        iterator = range(0, 5)
        diff_list = list(range(3, 5))

        root = Path("/tmp/app")

        for i in iterator:
            path = f"scenario_{i}.py"
            scn = create_scenario(root / path)
            scenarios.append(VirtualScenario(scn, []))

            if i in diff_list:
                scenarios_paths.append(f"scenario_{i}.py")

    with when:
        all_indexes, diff_indexes = get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert all_indexes == list(iterator)
        assert diff_indexes == diff_list


def test_one_diff_index_contained_in_one_all_indexes():
    with given:
        scenarios_paths = ["scenario_0.py"]

        path = Path("/tmp/app/scenario_0.py")
        scenarios = [VirtualScenario(create_scenario(path), [])]

    with when:
        all_indexes, diff_indexes = get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert all_indexes == [0]
        assert diff_indexes == [0]


def test_diff_indexes_not_contained_in_all_indexes():
    with given:
        scenarios_paths = ["scenario_0.py"]

        path = Path("/tmp/app/scenario_1.py")
        scenarios = [VirtualScenario(create_scenario(path), [])]

    with when, raises(BaseException) as exc_info:
        get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert exc_info.type is AssertionError
        assert str(exc_info.value) == "The selected scripts are not contained " \
                                      "in the selected tests folder!"


@pytest.mark.parametrize("scenarios", [None, list()])
def test_empty_all_indexes(scenarios: List or None):
    with given:
        scenarios_paths = ["scenario_0.py"]

    with when, raises(BaseException) as exc_info:
        get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert exc_info.type is AssertionError
        assert str(exc_info.value) == "Scenarios not found!"


@pytest.mark.parametrize("scenarios_paths", [None, list()])
def test_empty_diff_indexes(scenarios_paths: List or None):
    with given:
        scenarios = ["banana"]

    with when, raises(BaseException) as exc_info:
        get_indexes_of_scenarios(scenarios, scenarios_paths)

    with then:
        assert exc_info.type is AssertionError
        assert str(exc_info.value) == "Paths of scenarios not found!"
