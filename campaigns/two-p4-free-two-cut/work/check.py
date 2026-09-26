"""Independent 3P2-free and 2P4-free 2-Cut oracles."""

import argparse
import json
import random
import subprocess
import sys
from collections import deque
from itertools import combinations,product
from pathlib import Path

import z3


def adjacency(instance):
    neighbors = [set() for _ in range(instance["vertices"])]
    for u,v in instance["edges"]:
        neighbors[u].add(v)
        neighbors[v].add(u)
    return neighbors


def connected_simple(instance):
    if not isinstance(instance,dict):
        return False
    n,edges = instance.get("vertices"),instance.get("edges")
    if type(n) is not int or n < 1 or not isinstance(edges,list):
        return False
    seen_edges = set()
    for edge in edges:
        if (not isinstance(edge,list) or len(edge) != 2
                or any(type(v) is not int or not 0 <= v < n for v in edge)
                or edge[0] == edge[1]):
            return False
        key = tuple(sorted(edge))
        if key in seen_edges:
            return False
        seen_edges.add(key)
    neighbors = adjacency(instance)
    seen,queue = {0},deque([0])
    while queue:
        for v in neighbors[queue.popleft()]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return len(seen) == n


def contains_3p2(instance):
    if instance["vertices"] < 6:
        return False
    neighbors = adjacency(instance)
    for edges in combinations(instance["edges"],3):
        vertices = {v for edge in edges for v in edge}
        if len(vertices) == 6 and all(len(neighbors[v] & vertices) == 1 for v in vertices):
            return True
    return False


def contains_2p4(instance):
    if instance["vertices"] < 8:
        return False
    neighbors = adjacency(instance)
    paths = set()

    def extend(path):
        if len(path) == 4:
            paths.add(min(tuple(path),tuple(reversed(path))))
            return
        for v in neighbors[path[-1]]:
            if v in path or any(v in neighbors[u] for u in path[:-1]):
                continue
            extend(path+[v])

    for start in range(instance["vertices"]):
        extend([start])
    paths = list(paths)
    for i,first in enumerate(paths):
        first_set = set(first)
        for second in paths[i+1:]:
            if first_set.isdisjoint(second) and all(
                    v not in neighbors[u] for u in first for v in second):
                return True
    return False


def legal_source(source):
    return connected_simple(source) and not contains_3p2(source)


def legal_target(target):
    return connected_simple(target) and not contains_2p4(target)


def direct_cut(instance,side):
    n = instance["vertices"]
    return (isinstance(side,list) and len(side) == n
            and all(type(value) is bool for value in side)
            and any(side) and not all(side)
            and all(sum(side[u] != side[v] for v in neighbors) <= 2
                    for u,neighbors in enumerate(adjacency(instance))))


def cut_solutions(instance,source=False,limit=3):
    if not (legal_source(instance) if source else legal_target(instance)):
        raise ValueError("Illegal forbidden-subgraph 2-Cut instance")
    n = instance["vertices"]
    side = [z3.Bool(f"side_{v}") for v in range(n)]
    solver = z3.Solver()
    solver.add(z3.Or(*side),z3.Or(*[z3.Not(value) for value in side]))
    for u,neighbors in enumerate(adjacency(instance)):
        solver.add(z3.Sum(*[z3.If(side[u] != side[v],1,0) for v in neighbors]) <= 2)
    outputs = []
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive 2-Cut solver: {result}")
        model = solver.model()
        bits = [z3.is_true(model.eval(value)) for value in side]
        if not direct_cut(instance,bits):
            raise AssertionError("Z3 cut violates direct predicate")
        outputs.append({"side":bits})
        solver.add(z3.Or(*[value != bit for value,bit in zip(side,bits)]))
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_source(source):
    return cut_solutions(source,source=True,limit=1)[0]


def solve_target(target):
    return cut_solutions(target,source=False,limit=1)[0]


def valid_source(source,output):
    if not legal_source(source) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_source(source) == output
    return set(output) == {"side"} and direct_cut(source,output["side"])


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return set(output) == {"side"} and direct_cut(target,output["side"])


def exhaustive_cut(instance):
    for bits in product((False,True),repeat=instance["vertices"]):
        if direct_cut(instance,list(bits)):
            return {"side":list(bits)}
    return {"status":"NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases

    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for source,expected in EDGE_CASES:
        assert ("side" in solve_source(source)) == expected
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        assert ("side" in current) == ("side" in case["expected"]) == ("side" in exhaustive_cut(source))
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    checked,seen = 0,set()
    for seed in range(200):
        rng = random.Random(seed)
        n = rng.randint(2,9)
        edges = [[0,v] for v in range(1,n)]
        edges += [[u,v] for u in range(1,n) for v in range(u+1,n) if rng.randrange(2)]
        target = {"vertices":n,"edges":edges}
        key = json.dumps(target,sort_keys=True)
        if key not in seen and legal_target(target):
            seen.add(key)
            assert ("side" in solve_target(target)) == ("side" in exhaustive_cut(target))
            checked += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {checked} exhaustive 2P4-free target graphs")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal 2P4-free target: {target}")
        for output in cut_solutions(target):
            if not valid_target(target,output):
                raise AssertionError(f"Invalid target oracle output: {output}")
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
