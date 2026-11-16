import json
import pytest

RULE="All proposed plans must store customer data only within European Union regions."

def create(h):
    c=h.contract
    c.open_decision("decision-001","Choose a safe cloud migration strategy for a regional service.",RULE)
    c.add_option("decision-001","fast","Fast migration","Keep customer records in EU Frankfurt storage and use automated exports.",80,4)
    c.add_option("decision-001","cheap","Cheap migration","Keep customer records in EU Paris storage and use manual exports.",40,10)
    c.add_option("decision-001","slow","Slow migration","Keep customer records in EU Dublin storage with manual exports.",90,12)
    c.add_option("decision-001","unsafe","Unsafe migration","Send customer records to a non-EU US storage region.",10,2)
    c.seal_decision("decision-001")
    return c

def flags(h):
    h.response={"eligible":{"fast":True,"cheap":True,"slow":True,"unsafe":False}}

def test_pareto_retains_incomparable_options(host):
    h=host;c=create(h);flags(h)
    c.evaluate("decision-001")
    d=json.loads(c.get_decision("decision-001"))
    assert d["frontier"]==["cheap","fast"]
    assert d["excluded"]==["slow","unsafe"]
    assert d["state"]=="EVALUATED"
    with pytest.raises(h.error,match="Only Pareto frontier"):
        c.select_frontier_option("decision-001","slow")
    c.select_frontier_option("decision-001","cheap")
    assert json.loads(c.get_decision("decision-001"))["chosen"]=="cheap"
    with pytest.raises(h.error,match="Not open for selection"):
        c.select_frontier_option("decision-001","fast")

def test_independent_validator_rejects_disagreement(host):
    h=host;c=create(h);flags(h);c.evaluate("decision-001")
    vm=c.evaluate.__func__.__globals__["gl"].vm
    good={"fast":True,"cheap":True,"slow":True,"unsafe":False}
    assert h.validator(vm.Return(good)) is True
    h.response={"eligible":{"fast":True,"cheap":True,"slow":True,"unsafe":True}}
    assert h.validator(vm.Return(good)) is False

def test_missing_or_invalid_ai_flags_never_persist(host):
    h=host;c=create(h)
    for bad in ({"fast":True},{"fast":True,"cheap":True,"slow":True,"unsafe":"false"},
                {"fast":True,"cheap":True,"slow":True,"unsafe":False,"ghost":True}):
        h.response={"eligible":bad}
        with pytest.raises(h.error):c.evaluate("decision-001")
    assert json.loads(c.get_decision("decision-001"))["state"]=="SEALED"

def test_all_ineligible_has_empty_frontier(host):
    h=host;c=create(h)
    h.response={"eligible":{"fast":False,"cheap":False,"slow":False,"unsafe":False}}
    c.evaluate("decision-001")
    assert json.loads(c.get_decision("decision-001"))["frontier"]==[]
    with pytest.raises(h.error):c.select_frontier_option("decision-001","fast")

def test_lifecycle_owner_and_bounds(host):
    h=host;c=h.contract
    c.open_decision("decision-001","Choose a safe cloud migration strategy for a regional service.",RULE)
    with pytest.raises(h.error,match="Duplicate decision"):
        c.open_decision("decision-001","Choose a safe cloud migration strategy for a regional service.",RULE)
    with pytest.raises(h.error,match="Need at least two options"):
        c.seal_decision("decision-001")
    h.set_sender("0xOTHER")
    with pytest.raises(h.error,match="Only decision owner"):
        c.add_option("decision-001","fast","Fast plan","Plan uses EU hosted storage and isolated processing.",30,3)
    h.set_sender("0xOWNER")
    c.add_option("decision-001","fast","Fast plan","Plan uses EU hosted storage and isolated processing.",30,3)
    with pytest.raises(h.error,match="Duplicate option"):
        c.add_option("decision-001","fast","Fast plan","Plan uses EU hosted storage and isolated processing.",30,3)
    with pytest.raises(h.error,match="Invalid metrics"):
        c.add_option("decision-001","zero","Zero plan","Plan uses EU hosted storage and isolated processing.",0,3)
    c.add_option("decision-001","cheap","Cheap plan","Plan uses EU hosted storage with manual processing.",20,9)
    c.seal_decision("decision-001")
    with pytest.raises(h.error,match="Decision already sealed"):
        c.add_option("decision-001","third","Third plan","Plan uses EU hosted storage and isolated processing.",20,3)
    with pytest.raises(h.error,match="Already sealed"):
        c.seal_decision("decision-001")
    h.set_sender("0xOTHER")
    with pytest.raises(h.error,match="Only decision owner"):
        c.evaluate("decision-001")

def test_dominated_equal_and_tradeoff_math(host):
    from pathlib import Path
    import importlib.util
    p=Path(__file__).parents[2]/"contracts"/"ScenarioFork.py"
    spec=importlib.util.spec_from_file_location("pareto_module",p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    opts={"A":{"cost_units":10,"time_units":12},"B":{"cost_units":12,"time_units":10},"C":{"cost_units":14,"time_units":14},"D":{"cost_units":10,"time_units":12}}
    assert m.pareto_frontier(opts,{k:True for k in opts})==["A","B","D"]
    assert m.pareto_frontier(opts,{k:False for k in opts})==[]
