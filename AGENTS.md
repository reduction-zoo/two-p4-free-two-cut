# Research instructions

Read the [fixed question](campaigns/two-p4-free-two-cut/question.md), [prior state](campaigns/two-p4-free-two-cut/state.md) and [preparation notes](campaigns/two-p4-free-two-cut/work/preparation.md). The fixed [test corpus](campaigns/two-p4-free-two-cut/work/cases.json) and [verifier](campaigns/two-p4-free-two-cut/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/two-p4-free-two-cut/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Scope and budgets in the state describe earlier work and do not limit a new campaign. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
