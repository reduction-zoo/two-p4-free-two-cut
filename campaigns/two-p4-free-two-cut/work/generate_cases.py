"""Fix seeded connected 3P2-free 2-Cut instances before construction."""

import json
import random
from pathlib import Path


def graph(n,edges):
    return {"vertices":n,"edges":edges}


def clique(n):
    return [[u,v] for u in range(n) for v in range(u+1,n)]


EDGE_CASES = [
    (graph(1,[]),False), (graph(2,[[0,1]]),True),
    (graph(3,clique(3)),True), (graph(4,clique(4)),True),
    (graph(5,clique(5)),False),
    (graph(6,[[i,i+1] for i in range(5)]),True),
    (graph(6,[[i,i+1] for i in range(5)]+[[0,5]]),True),
    (graph(6,[[0,i] for i in range(1,6)]),True),
    (graph(6,clique(6)),False),
    (graph(5,clique(4)+[[0,4]]),True),
    (graph(4,[[0,1],[1,2],[2,3]]),True),
    (graph(5,[[0,1],[1,2],[2,3],[3,4]]),True),
]


def random_source(seed):
    rng = random.Random(seed)
    if seed % 2 == 0:
        n = rng.randint(6,8)
        edges = clique(3)
        edges += [[0,v] for v in range(3,n)]
        edges += [[u,v] for u in (1,2) for v in range(3,n-1)
                  if rng.randrange(2)]
    else:
        n = rng.randint(5,8)
        edges = clique(n)
        removable = rng.sample(edges,rng.randint(0,2))
        edges = [edge for edge in edges if edge not in removable]
    return graph(n,sorted(edges))


def build_cases():
    from check import solve_source
    cases,seen = [],set()

    def add(source,kind,seed=None,hand_answer=None):
        key = json.dumps(source,sort_keys=True,separators=(",", ":"))
        if key in seen:
            return False
        seen.add(key)
        answer = solve_source(source)
        if hand_answer is not None and ("side" in answer) != hand_answer:
            raise AssertionError(f"Hand label disagrees with oracle: {source}")
        case = {"source":source,"kind":kind,"expected":answer}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for source,expected in EDGE_CASES:
        add(source,"edge",hand_answer=expected)
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed),"random",seed=seed)
        seed += 1
    return cases


if __name__ == "__main__":
    path = Path(__file__).with_name("cases.json")
    cases = build_cases()
    path.write_text(json.dumps(cases,indent=2)+"\n")
    print(f"Wrote {len(cases)} cases to {path}")
