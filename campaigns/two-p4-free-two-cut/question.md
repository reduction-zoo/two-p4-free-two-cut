# 3P2-free 2-Cut → 2P4-free 2-Cut

Category: Complexity open

## Source

The source is a connected graph containing no induced disjoint union of three edges. Its outputs are nontrivial cuts with crossing degree at most two, or NO-SOLUTION.

## Target

Both problems seek a nontrivial cut with at most two opposite neighbors per vertex in a connected simple graph. The source is 3P2-free and the target has no induced disjoint union of two four-vertex paths.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

This addresses a remaining forbidden-induced-subgraph case for bounded-degree cuts.

## Difficulty

Connecting gadgets must eliminate pairs of induced paths while preserving all legal cut choices.

## Literature context

The cited induced-subgraph classification leaves the 2P4-free case distinct from the known 3P2-free source case.

Literature checked 2026-09-14. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [Finding d-Cuts in Graphs of Bounded Diameter, Graphs of Bounded Radius and H-Free Graphs](https://eprints.cs.univie.ac.at/8514/1/Finding_d_cuts_in_Graphs_ALGORITMICA.pdf): - R1. Lucke, Momeni, Paulusma, Smith, Finding d-Cuts in Graphs of Bounded Diameter, Graphs of Bounded Radius and H-Free Graphs, Algorithmica 88:7 (2026), Theorems 5 and 13, Section 5 (PDF page 25). - R11. Dabrowski, Eagling-Vose, Johnson, Paesani, Paulusma, Finding d-Cuts in Probe H-Free Graphs, arXiv:2505.22351v1, 28 May 2025, Theorems 1.1 and 1.4.
- [Finding d-Cuts in Probe H-Free Graphs](https://arxiv.org/html/2505.22351): - R1. Lucke, Momeni, Paulusma, Smith, Finding d-Cuts in Graphs of Bounded Diameter, Graphs of Bounded Radius and H-Free Graphs, Algorithmica 88:7 (2026), Theorems 5 and 13, Section 5 (PDF page 25). - R11. Dabrowski, Eagling-Vose, Johnson, Paesani, Paulusma, Finding d-Cuts in Probe H-Free Graphs, arXiv:2505.22351v1, 28 May 2025, Theorems 1.1 and 1.4.

Fixed from board record `website/questions/two-p4-free-two-cut.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
