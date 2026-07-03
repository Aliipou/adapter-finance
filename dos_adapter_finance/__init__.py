"""Decision OS execution adapter for finance. EXPERIMENTAL.

Governed financial tools (payments, transfers, trades) reached ONLY when the
kernel permits. Pairs naturally with plugin-approval: a large payment is gated by
the kernel AND held for a human. Bodies are honest stubs — wire the real
payment/brokerage SDK where marked. Holds no authority.
"""

from __future__ import annotations

from typing import Any


def approve_payment(amount, payee) -> str:
    # TODO: wire the real payments SDK (Stripe, bank API) here.
    return f"[finance] payment {amount} -> {payee} approved"


def transfer_funds(amount, src, dest) -> str:
    # TODO: wire the real banking SDK here.
    return f"[finance] transfer {amount} {src} -> {dest}"


def place_trade(symbol, side, qty) -> str:
    # TODO: wire the real brokerage SDK here.
    return f"[finance] {side} {qty} {symbol}"


def issue_refund(amount, order_id) -> str:
    # TODO: wire the real payments SDK here.
    return f"[finance] refund {amount} for {order_id}"


TOOLS = {"approve_payment": approve_payment, "transfer_funds": transfer_funds,
         "place_trade": place_trade, "issue_refund": issue_refund}
SPECS: dict[str, dict[str, Any]] = {
    "approve_payment": {"capability": "tool:approve_payment"},
    "transfer_funds": {"capability": "tool:transfer_funds"},
    "place_trade": {"capability": "tool:place_trade"},
    "issue_refund": {"capability": "tool:issue_refund"},
}


def governed_tools(governor: Any) -> dict[str, Any]:
    """Wrap these finance tools with a decision_os_min.Governor so every call is
    authorized + audited. Returns the governed tool registry."""
    return governor.wrap(TOOLS, specs=SPECS)
