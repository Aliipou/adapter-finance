import pytest
from decision_os_min import GovernanceRefused, Governor, set_actor

from dos_adapter_finance import governed_tools

POLICY = {"grants": {"agent:ops": ["tool:approve_payment"]}, "default": "deny"}


def _gov(tmp_path):
    return Governor(POLICY, audit_path=str(tmp_path / "a.jsonl"))


def test_permitted_payment_reaches_the_actuator(tmp_path):
    tools = governed_tools(_gov(tmp_path))
    set_actor("agent:ops")
    assert "approved" in tools["approve_payment"](amount=100, payee="x")


def test_ungranted_finance_action_never_executes(tmp_path):
    tools = governed_tools(_gov(tmp_path))
    set_actor("agent:ops")                       # has approve_payment, NOT place_trade
    with pytest.raises(GovernanceRefused):
        tools["place_trade"](symbol="AAPL", side="buy", qty=10)


def test_unauthorized_actor_never_executes(tmp_path):
    tools = governed_tools(_gov(tmp_path))
    set_actor("agent:intruder")
    with pytest.raises(GovernanceRefused):
        tools["approve_payment"](amount=100, payee="x")
