# Preparation evidence

Prepared on 2026-09-26 before construction. The fixed corpus has 112
distinct legal connected 3P2-free graphs: 12 hand-labelled edge cases and
100 seeded random cases, with 70 YES and 42 NO decisions and one to eight
vertices. This question has the same source language as the P6-free 2-Cut
question, so the fixed source cases and generator are reproduced in this
independent repository. `generate_cases.py` retains seeds; `cases.json`
stores checked cuts or NO-SOLUTION. Source legality is checked by testing
every triple of disjoint graph edges for the required induced matching.
Z3 4.16.0 encodes a nontrivial two-side partition with crossing degree at
most two. Returned cuts are checked by direct neighbor counting. UNSAT
is conclusive; unknown is an error. Exhaustive side assignments agreed
on all 112 source cases.

The target promise is checked by enumerating induced four-vertex paths,
then testing disjoint pairs for the absence of all cross edges. This is
exactly an induced `2P4`. The same cut encoding is used with separate
target legality. Independent exhaustive side assignments agreed with Z3
on 129 distinct 2P4-free connected graphs with up to nine vertices. Hand
fixtures cover YES on K4, NO on K5, an illegal graph containing two
induced P4s connected through a ninth vertex, a legal eight-vertex path,
and malformed or invalid cuts.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/two-p4-free-two-cut/work/check.py --self-test
```

The self-test starts with the corpus gate, regenerates seeded graphs,
rechecks labels and witnesses, and compares target decisions to exhaustive
enumeration. The candidate runner uses separate forward and recovery
subprocesses and up to three target cuts per source. An incorrect injected
candidate was rejected after target solving and source validation. No
actual reduction candidate exists; finite checks do not establish
hardness or a general reduction.
