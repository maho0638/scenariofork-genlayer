"""Real Studionet integration: deploy, evaluate plans with unmocked validator consensus, verify state.

Only ephemeral auto-created accounts. No user keys, model mocks, or value transfer.
"""
import json
import os
from gltest import get_contract_factory, get_default_account
from gltest.assertions import tx_execution_succeeded

def record(message):
    print("STUDIONET_PROOF:", message, flush=True)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("- " + message + "\n")

def send(contract_call, name):
    receipt = contract_call.transact(wait_interval=2000, wait_retries=50)
    assert tx_execution_succeeded(receipt), receipt
    record(name + " receipt " + str(receipt.get("hash", receipt.get("transaction_hash", receipt.get("id", "unavailable")))))

def test_scenariofork_real_studionet():
    account = get_default_account()
    record("NETWORK studionet (RPC https://studio.genlayer.com/api, chain ID 61999)")
    record("DEPLOYER " + account.address + " (ephemeral; no key stored)")
    factory = get_contract_factory("ScenarioFork")
    contract = factory.deploy(args=[], account=account, wait_interval=2000, wait_retries=50)
    record("CONTRACT " + str(contract.address))
    decision_id = "qa-studio-decision-20261116"
    send(contract.open_decision(args=[
        decision_id, "Choose a compliant storage migration within the EU.",
        "All customer records must remain in an EU data-center region."
    ]), "OPEN_DECISION")
    send(contract.add_option(args=[
        decision_id, "fast", "Frankfurt migration",
        "All customer records stay in the EU Frankfurt data center with automated migration.",
        80, 4
    ]), "ADD_FAST")
    send(contract.add_option(args=[
        decision_id, "cheap", "Dublin migration",
        "All customer records remain in the EU Dublin data center with manual migration.",
        40, 10
    ]), "ADD_CHEAP")
    send(contract.seal_decision(args=[decision_id]), "SEAL")
    sealed = json.loads(contract.get_decision(args=[decision_id]).call())
    assert sealed["state"] == "SEALED"
    assert set(sealed["option_ids"]) == {"fast", "cheap"}

    # Genuine GenLayer AI transaction: no mocks, leader_only=false, max 3 rotations.
    receipt = contract.evaluate(args=[decision_id]).transact(
        consensus_max_rotations=3, wait_interval=2000, wait_retries=80
    )
    assert tx_execution_succeeded(receipt), receipt
    record("EVALUATE receipt " + str(receipt.get("hash", receipt.get("transaction_hash", receipt.get("id", "unavailable")))))
    evaluated = json.loads(contract.get_decision(args=[decision_id]).call())
    assert evaluated["state"] == "EVALUATED"
    assert set(evaluated["eligible"]) == {"fast", "cheap"}
    assert all(type(v) is bool for v in evaluated["eligible"].values())
    assert set(evaluated["frontier"]) <= {"fast", "cheap"}
    record("RESULT eligible=" + json.dumps(evaluated["eligible"], sort_keys=True)
           + " frontier=" + json.dumps(evaluated["frontier"]))
    record("SUCCESS actual on-network deploy/write/read/AI-consensus without mocks")
