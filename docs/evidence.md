# Interpretation of the finite evidence

## Exact checks and manuscript locations

The corresponding article includes all essential proofs. Standalone proof numbering is stable within `proofs/theory.md`, and need not match article numbering.

| Statement | Proof note | Article |
|---|---|---|
| Generator extension and composition | Proposition 1 | Section 2 |
| Known-context cancellation; joint-coverage converse | Propositions 2–3 | Section 3 |
| Reversible masking and soundness distinction | Propositions 4–5 | Section 3, Figure 1 |
| Closure identification and scalar capacity | Theorem 6, Corollary 7 | Theorem 4.3, Corollary 4.4, Figure 2 |
| Asymmetric transport cancellation | Lemma 8 | Theorem 4.2, Table 1 |
| Nested closure reflection | Theorem 9 | Theorem 5.2 |
| Reversible reflection and factorization count | Theorem 10 | Theorem 6.1 |
| Counter stabilizers and restricted optimum | Lemma 11, Theorem 12 | Lemma 7.1, Theorem 7.2 |
| Witness and finite checking contract | Propositions 13–14 | Section 8 |

## Closure and transport universes

`closure_verification.json` records all seven, sixty-one, and 115 closures on the four-, eight-, and nine-state domains. The independent checker enumerates extensive maps, rather than reuse the producer's meet-closed fixed-point subsets. It tests respectively 20, 887, and 4,116 monotone scalar observations into a height-sized chain. Exactly one in each universe separates comparable pairs and identifies all closures: the height rank. This exact uniqueness is only for those enumerated codomains and domains.

Nested ordered closure pairs number 22, 733, and 1,992. Equal-rank defects detected after a source application number 2, 588, and 2,138. Table 2 reports these quantities. They are ordered function/input checks, not independent experimental subjects.

`transport_verification.json` enumerates 36 monotone B2 transports, twelve extensive idempotent sources, and nine monotone extensive targets: 3,888 triples and 15,552 point squares. There are 6,768 underlying defects, including 240 equal-rank first-input defects repaired by the second test. All 779 equal observed profiles have equal underlying maps. Its five controls each violate exactly one of the retained source/transport/target hypotheses while preserving the others.

## Reversible and count-probe universes

`reversible_verification.json` enumerates 256 three-gate factorizations of identity over four program objects on B2. Four are locally natural. The numbers passing observation are 256 with no probes, 256 with rank at both cuts, 32 with a rigid probe only at the first cut, and four with rigid probes at both cuts. These are exact counts over the stated group, not frequencies in real analysis implementations.

`probe_verification.json` covers all fifty naturally labelled posets on one through four points (1, 2, 7, 40). It independently checks 11,480 ordered support families through the first feasible cardinality. These are not fifty nonisomorphic posets. Arbitrary state encodings, weighted counts, dynamic probes, and bit-level instrumentation cost are outside the optimum.

## Graph corpus and comparison methods

The corpus consists of 36 domain/shape/variant cases, correlated-input and nonidentity-transport controls, twelve nested-closure cases, one nonnested control, three bounded scaling cases, and three nonbijective-transport controls. All generated cases and certificates are bundled. The latter three test a strengthened transport hypothesis; they were not selected to make a performance comparison favorable.

Forty cases have a local defect. Ordinary final-output checking detects nine and legitimately accepts the other thirty-one for its own property. Checking all generator-local squares detects all forty using 15,044 equations, whereas all-arrow local enumeration uses 33,876 equations. This is an instance of generator completeness, not a new performance algorithm.

Ordinary outputs plus the supplied probes detect thirty-four of the forty defects. The remaining six are three flat-observer closure cases, the correlated-input example, the nonnested closure example, and the source-nonidempotence transported example. Each lies outside a hypothesis of the applicable converse. They remain in the results.

Sampling eight distinct generator/node/input triples under each seed 0–31 detects 736 of 1,280 defective-case/seed pairs. Per-case detections range from four to thirty-two seeds. Sampling uses fewer equations and does not certify absence of a local defect. No equal-work speedup, significance test, population generalization, or confidence interval is claimed.

Table 3 uses the three scaling inputs ending in `1-2`, `2-10`, and `3-20`. Their `(objects, arrows, nodes, maximum states)` are `(2,3,2,4)`, `(4,9,10,8)`, and `(8,27,20,32)`. Combined counts are 48, 2,088, and 67,392. Compact certificate summaries are 148–173 bytes; the largest input has 75,474 bytes. Small certificate size does not make the exhaustive checker constant-time.

## Measurement scope and comparison

`reproduction_measurements.json` and `measured_job_logs/` preserve the recorded nine-job run supporting the manuscript's resource sentence. CPU totals include process startup; the wall interval within a job starts immediately before the project script. Per-case timers in `case_measurements.json` measure checker work only. Maximum single-job RSS is not claimed to be an exact aggregate process-tree peak. These distinct clocks should not be substituted for one another.

The runner regenerates and directly compares 58 case/certificate files and nine deterministic scientific result files. Clocks are excluded from comparison, as are the original pilot measurement records. The raw JSON/CSV equality check is used instead of a hash manifest. No exact historical CPU total is available for all earlier interactive prototypes.

## Scientific scope

The equalities are finite checks, not machine-checked general proofs. The nonbijective asymmetric lemma has a complete written proof; its small oracle attacks its hypotheses but does not establish the theorem merely by test count. The full-interval counterexample and the extensive-automorphism argument keep the semantic interpretations honest.

No other portfolio project's code, fixtures, proof text, or result cache is required. Primary research papers are used for attribution and mathematical comparison only. Venue-level originality remains a research-readiness question separate from successful reproduction.

A separate clean archive extraction repeated the documented runner and paper build successfully. `extraction_verification.json` and `extraction_job_logs/` retain that run. Its clocks are a second measurement, not replacements for the manuscript's recorded measurement. All 21 rebuilt manuscript pages matched the previously inspected rendering.
