# Cancellability Conditions

Finite evidence and self-contained proofs for **Observation-Relative Cancellability for Compositional Algebraic Analyses**.

The repository is a standalone companion to the manuscript. It contains no private data, network dependency, external solver, or hidden controller. Python 3 and the standard library are sufficient.

## Reproduce the evidence

From this directory, use a fresh output path:

```sh
python reproduce.py --output reproduction
```

The runner executes nine sequential bounded jobs with one child process at a time. It reconstructs all 63 graph cases, independently checks their certificates, rebuilds and verifies the closure and count-probe universes, runs the exact reversible and transported-square oracles, and executes 41 regression tests. It then compares 73 deterministic JSON/CSV evidence files directly with the bundled results. Timing measurements are recorded but excluded from equality checks.

Expected scientific summary:

| Quantity | Value |
|---|---:|
| Graph cases | 63 |
| Locally natural cases | 20 |
| Ordinarily globally natural cases | 54 |
| Local defects hidden at final outputs | 34 |
| Local equations checked | 35,010 |
| Ordinary-global equations checked | 4,464 |
| Probe equations checked | 61,164 |
| Total equations | 100,638 |
| Regression tests | 41 |
| Directly compared deterministic files | 73 |

The largest case has 67,392 equations and 75,474 input bytes. Compact certificates range from 148 to 175 bytes. Every producer certificate is recomputed extensionally before acceptance.

## What the results establish

The mathematical argument distinguishes four interfaces.

* A general DAG has a sufficient converse when node outputs are jointly separated and every formal parent tuple is reached.
* Closure operators require exactly separation of strict comparable pairs. The transported theorem needs an extensive idempotent source, a monotone extensive target, and a monotone transport; a defect is observed at `x` or after one source application.
* Nested unary closure forests use absorption to collapse every root-to-node path, so the closure theorem reflects all local squares without prefix surjectivity. Branching is allowed; merge nodes are not.
* Reversible pipelines with identity transports require trivial observation stabilizers. The remaining compatible factorizations have an exact finite-group count.

For finite distributive lattices, the minimum number of permitted unweighted subset-count probes is `ceil(log2 D(P))`, where `D(P)` is the distinguishing number of the join-irreducible poset. Rank identifies every closure in the selected universes while preserving all lattice automorphisms, demonstrating that closure and reversible interfaces are genuinely different.

## Evidence map

| Path | Role |
|---|---|
| `proofs/theory.md` | Complete proof note and model boundaries |
| `src/checker.py` | Structural validation and independent extensional certificate checking |
| `src/construct.py` | Deterministic graph-case producer, including closure forests |
| `src/campaign.py` | Corpus evaluation, controls, and sampling comparison |
| `src/closure_search.py`, `src/closure_checker.py` | Independent closure and observer enumeration paths |
| `src/transport_oracle.py` | Asymmetric transported-square universe and five hypothesis controls |
| `src/reversible_oracle.py` | Exact reversible-factorization count |
| `src/probe_search.py`, `src/probe_checker.py` | Candidate and independent verification paths for count probes |
| `tests/test_checker.py` | Positive, negative, parser, resource, and certificate tests |
| `cases/` | Canonical 63 finite instances and certificates |
| `results/campaign_summary.json` | Corpus totals |
| `results/case_verification.json` | Per-case recomputed verdicts, witnesses, and controls |
| `results/closure_verification.json` | Exhaustive closure/observer universes |
| `results/transport_verification.json` | Transported theorem and assumption-removal evidence |
| `results/reversible_verification.json` | Reversible count evidence |
| `results/probe_verification.json` | Count-probe optimum evidence |
| `claim_evidence_ledger.csv` | Claim-to-proof/check/result mapping |
| `external_resources.csv` | Scholarly and official resource inventory |

## Resource and portability boundaries

The recorded clean non-resumed run used 7.955369 aggregate child CPU seconds and a maximum single-job peak resident set of 97,968 KiB. These values cover the nine measured jobs only; they are not a retrospective total for all earlier proof development, editing, compilation, or packaging. Per-case timing is descriptive and never part of deterministic equality.

The runner rejects a nonempty output unless `--resume` is explicitly supplied. Final validation must not use resume. Scientific children are bounded by an external 120-second timeout and a three-gibibyte address-space limit. Inputs are additionally capped by dimensions and equation counts in the checker.

## Interpretation limits

The program category contains semantics-preserving insertions of labelled `skip` instructions. Extensive closures on three finite abstract domains are sound coarsenings of the identity transformer. Reversible mutations and nonidentity transports are algebraic controls, not production-analyzer or deployed-CFG claims. The repository does not establish performance, industrial representativeness, arbitrary recursive composition, infinite-domain results, or a bridge to a different categorical robustness semantics.

The producer and verifier are separately implemented but share a specification and development history. Passing commands show deterministic agreement for the declared finite model; they are not proof-assistant verification or independent external review.

## License and attribution

Repository code and proof text are covered by `LICENSE`. External scholarly works are cited rather than redistributed. The publisher class and bibliography style live only in the manuscript package, with their original notices retained.
