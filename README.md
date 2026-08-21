# adapter-finance

**Live (graph):** [https://ali-adapter-finance.vercel.app](https://ali-adapter-finance.vercel.app)

Decision OS / AuthGate **execution adapter** for financial actions (payments,
transfers, trades, refunds). It exposes each action as a **governed tool**: the
effect *behind* a Policy Enforcement Point, reached only when the
`decision-os-min` kernel authorizes the action. The adapter holds **no
authority** of its own and never bypasses the kernel — every call is authorized
and audited.

> Part of the Decision OS — governed by the Legitimacy ⊥ Authority pipeline
> (FDK legitimacy → AuthGate authority). Adapters adapt tools into governed
> effects and hold **no authority** of their own.

## What it adapts

| Tool | Capability | Effect |
|------|------------|--------|
| `approve_payment` | `tool:approve_payment` | Approve a payment to a payee |
| `transfer_funds` | `tool:transfer_funds` | Transfer funds between accounts |
| `place_trade` | `tool:place_trade` | Place a trade (symbol/side/qty) |
| `issue_refund` | `tool:issue_refund` | Issue a refund for an order |

## Install

```bash
pip install -e .          # brings in decision-os-min
# for development:
pip install -e ".[dev]"   # + pytest, ruff, mypy
```

## Usage

```python
from decision_os_min import Governor, set_actor
from dos_adapter_finance import governed_tools

policy = {"grants": {"agent:ops": ["tool:approve_payment"]}, "default": "deny"}
gov = Governor(policy, audit_path="audit.jsonl")
tools = governed_tools(gov)

set_actor("agent:ops")
tools["approve_payment"](amount=100, payee="acme")   # runs only if the kernel ALLOWs
```

Each financial action is a distinct capability, so a policy can grant refunds
without granting trades. An actor without the matching grant raises
`GovernanceRefused` before the effect runs. This pairs naturally with a
human-approval plugin in the kernel: a large payment can be gated by policy *and*
held for a human.

## Status & limitations

**Experimental / interface-only.** The tool bodies are honest stubs that return a
string describing the intended effect — they do **not** call any real payment,
banking, or brokerage SDK yet. Wire the real SDK at the `# TODO` markers in
`dos_adapter_finance/__init__.py`. What is real today is the governance wiring:
the capability→tool mapping and the fail-closed authorization boundary.

This is reference software handling a sensitive domain. It performs no amount
validation, idempotency, currency handling, or reconciliation. Review and test
thoroughly before any production use.

## License

PolyForm Noncommercial 1.0.0 (see `LICENSE`).
