"""Deliberately small stdlib-only fake host, NOT official GenLayer Direct Mode."""
import importlib.util
import json
import pathlib
import sys
import types
import pytest

class VMError(Exception):
    pass

class Return:
    def __init__(self, calldata):
        self.calldata = calldata

class Host:
    sender = "0xOWNER"
    response = {}
    validator = None
    prompt = ""
    def nondet(self, leader, validator):
        result = leader()
        self.validator = validator
        return result
    def llm(self, prompt, response_format):
        assert response_format == "json"
        self.prompt = prompt
        return self.response
    def check_validator(self, candidate=None):
        assert self.validator
        return self.validator(Return(self.response if candidate is None else candidate))

@pytest.fixture
def host(monkeypatch):
    host = Host()
    host.sender = "0xOWNER"
    host.response = {}
    host.validator = None
    public = types.SimpleNamespace(write=lambda f:f, view=lambda f:f)
    gl = types.SimpleNamespace(Contract=type("Contract", (), {}), public=public,
        message=types.SimpleNamespace(sender_address=None), vm=types.SimpleNamespace(
            UserError=VMError, Return=Return, run_nondet_unsafe=host.nondet),
        nondet=types.SimpleNamespace(exec_prompt=host.llm))
    def set_sender(who):
        host.sender = who
        gl.message.sender_address = who
    host.set_sender = set_sender
    set_sender("0xOWNER")
    class TreeMap(dict):
        def __class_getitem__(cls, arg):
            return cls
    module = types.ModuleType("genlayer")
    module.gl = gl
    module.TreeMap = TreeMap
    module.u256 = int
    monkeypatch.setitem(sys.modules,"genlayer",module)
    path = pathlib.Path(__file__).parents[2]/"contracts"/"ScenarioFork.py"
    spec = importlib.util.spec_from_file_location("scenariofork_under_test",path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    contract = mod.ScenarioFork()
    host.contract = contract
    host.error = VMError
    return host
