"""Official GenLayer Direct Mode tests. Requires genlayer-test; not offline stubs."""
import json

RULE = "All customer records must stay within European Union storage regions."


def setup(c):
    c.open_decision("decision-001", "Choose a reliable EU-only regional cloud migration plan.", RULE)
    c.add_option("decision-001", "fast", "Fast EU option", "Store customer records in the EU Frankfurt region with automatic migration.", 80, 4)
    c.add_option("decision-001", "cheap", "Cheap EU option", "Store customer records in the EU Dublin region with manual migration.", 40, 10)
    c.add_option("decision-001", "slow", "Slow EU option", "Store customer records in the EU Paris region with manual migration.", 90, 12)
    c.add_option("decision-001", "unsafe", "US location", "Store customer records on servers physically located in the US.", 10, 2)
    c.seal_decision("decision-001")


def mock(vm, eligible):
    vm.clear_mocks()
    vm.mock_llm(r"(?s).*ScenarioFork\. Check whether EACH proposed plan.*", json.dumps({"eligible": eligible}))


def test_frontier_and_validator(direct_vm, direct_deploy):
    c = direct_deploy("contracts/ScenarioFork.py")
    setup(c)
    good = {"fast": True, "cheap": True, "slow": True, "unsafe": False}
    mock(direct_vm, good)
    c.evaluate("decision-001")
    assert json.loads(c.get_decision("decision-001"))["frontier"] == ["cheap", "fast"]
    assert direct_vm.run_validator() is True
    mock(direct_vm, {"fast": True, "cheap": True, "slow": True, "unsafe": True})
    assert direct_vm.run_validator() is False
    with direct_vm.expect_revert("Only Pareto frontier is selectable"):
        c.select_frontier_option("decision-001", "slow")
    c.select_frontier_option("decision-001", "fast")
    assert json.loads(c.get_decision("decision-001"))["chosen"] == "fast"


def test_all_rejected_results_in_empty_frontier(direct_vm, direct_deploy):
    c = direct_deploy("contracts/ScenarioFork.py")
    setup(c)
    mock(direct_vm, {"fast": False, "cheap": False, "slow": False, "unsafe": False})
    c.evaluate("decision-001")
    assert json.loads(c.get_decision("decision-001"))["frontier"] == []


def test_malformed_response_cannot_change_state(direct_vm, direct_deploy):
    c = direct_deploy("contracts/ScenarioFork.py")
    setup(c)
    mock(direct_vm, {"fast": True, "cheap": True})
    with direct_vm.expect_revert("Missing or extra option"):
        c.evaluate("decision-001")
    assert json.loads(c.get_decision("decision-001"))["state"] == "SEALED"


def test_unauthorized_and_duplicate(direct_vm, direct_deploy, direct_bob):
    c = direct_deploy("contracts/ScenarioFork.py")
    c.open_decision("decision-001", "Choose a reliable EU-only regional cloud migration plan.", RULE)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("Only decision owner"):
        c.add_option("decision-001", "option-001", "Fast EU option", "Store all customer records in the EU region and encrypt them.", 30, 5)


def test_replay_and_sealed_manifest(direct_vm, direct_deploy):
    c = direct_deploy("contracts/ScenarioFork.py")
    setup(c)
    with direct_vm.expect_revert("Already sealed"):
        c.seal_decision("decision-001")
    with direct_vm.expect_revert("Decision already sealed"):
        c.add_option("decision-001", "new-one", "New alternative", "Store all customer records in the EU region and encrypt them.", 20, 6)
