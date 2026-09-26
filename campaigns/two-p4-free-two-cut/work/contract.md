# Prepared input and output contract

Both inputs use `{"vertices": n, "edges": [[u,v], ...]}` with a connected
simple undirected graph on `0..n-1`, `n >= 1`. The source contains no
induced disjoint union of three edges (`3P2`); the target contains no
induced disjoint union of two four-vertex paths (`2P4`). A positive
output is `{"side": [bool, ...]}`, a nontrivial two-side partition with
at most two opposite-side neighbors at each vertex. The alternative
`{"status": "NO-SOLUTION"}` is valid exactly when no such cut exists.
A connected one-vertex graph is legal but has no nontrivial cut.

A candidate `algorithm.py` reads source JSON from stdin and writes legal
target JSON to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes a valid source
output. The commands share no memory, exit nonzero on errors and send
diagnostics to stderr. They must be deterministic and polynomial time;
recovery must work for every valid target cut or negative answer.

`check.py --candidate PATH` independently solves each constructed target
on the fixed source corpus and validates recovered source cuts directly.
