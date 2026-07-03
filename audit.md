# Audit

Dated log of editorial passes and verification runs. Newest first.
See the workspace docs (run `papers docs`): writing-pipeline.md §7 and refresh-pipeline.md.

## 2026-07-01 — Initial implementation from seed chat
Scope: full paper built from `chats/chat.md` (a long ChatGPT thread evolving the sorites/heap question into a general "coarse-grained accumulation" architecture spanning subitization, action potentials, reservoir computing, and multicellularity) through the PIATRA pipeline.
Decision: to break the corpus fingerprint the instrument is reservoir computing / echo-state dynamics + the combinatorics of a non-transitive indistinguishability relation + critical-transition early warning, none used before. The headline results (a relation-collapse of 1 class vs 1000, and a "latent forewarns while the readout is silent" reversal) are a different result-shape from the corpus's thresholds and negative-IDs.
Changes:
  - Formal spine: x_{t+1}=F(x_t,u_t), y_t=R(x_t); the sorites condition R(x_{t+1})=R(x_t) while x_{t+1}!=x_t; the paradox = readout-invariance mistaken for state-invariance = non-transitive tolerance mistaken for transitive equivalence.
  - Simulation (numpy + matplotlib, uv, seeded SEED=20260701): (1) SUBTHRESHOLD SUMMATION — 60 leaky integrators; readout silent 37 steps (variance 0) while count grows 37x; latent decode R^2=1.0; (2) NON-TRANSITIVE INDISTINGUISHABILITY — adjacent rate 1.0, endpoints 333x tolerance, transitive closure 1 class vs 1000 true, 75% intransitive triples; (3) LOCAL TOLERANCE / GLOBAL TRANSITION — soft threshold, per-grain max 0.0062 vs total 1.0, borderline 175 (tight) vs 703 (loose); (4) CRITICAL TRANSITION — bistable across a fold, flip at 4483 with 0 readout warning, variance +15x, autocorrelation 0.9->0.99, critical-slowing lead 1450, reservoir alarm 198 steps ahead.
  - Calibration fix (Study 4): the fine integration dt saturated the lag-1 autocorrelation (~1 even at baseline), washing out critical slowing down; recomputed the early-warning indicators on a subsampled series (stride 25) and took the variance-crossing for the lead, which recovers the standard rising-AC/variance signature honestly.
  - Wrote PAPER.md (9 sections, argument-driven distinctive titles; §9 folds objections and states a conservative novelty boundary — shared architecture not ontology, not fuzzy logic, not mere thresholding; the sheaf reading taken only as far as "local readouts need not glue"). 21-source bibliography, all engaged in-text.
  - 23 candidates verified against journals/arXiv/SEP/DOI; corrections applied (SEP is Raffman & Hyde, latest ed.; Dzhafarov & Perry; Bonnasse-Gahot & Nadal in Neural Computation 2022). 0 confabulated. Caught and fixed a missing bibliography entry (Brunet & King 2017 was cited but absent) before the refs gate passed.
Verification:
  - voice: 0 errors, 14 review-candidate warns (negate-pivot / inline-contrastive, intrinsic). Thinned "exactly" (6 -> 2) and one "carries".
  - refs: 0 missing, 0 unused (21 in-text keys, 21 bib entries).
  - claims: 4 prose decimals, 0 without a matching results.json value.
  - build: clean, 0 missing-character warnings.
  - check => PASS

---

## 2026-07-03 — reform pass (de-oversell + de-template)

Corpus reform. The paper already disclosed the sheaf/contextuality reading as "only... the honest slogan that locally adequate readouts need not glue into one global predicate" and hedged the reservoir claims. Two genuine defects.

- paper/PAPER.md + metadata.yaml abstract, and §5: the R-squared of 1.0 was oversold ("holds the accumulated count so faithfully"). For a noiseless deterministic leaky integrator the state is a linear function of the accumulated input, so a linear decoder recovers it exactly by construction; the 1.0 is trivial, not a finding. Reframed to say the precision "is guaranteed by construction and is not the point; the point is qualitative, that the information the readout discards is not lost."
- paper/PAPER.md §9: retitled "What the Architecture Does and Does Not Claim" -> "One Design, Not Five Metaphors" (subthreshold was on the templated-closer census list), taking the title from the abstract's own synthesis claim; the shared-architecture-not-ontology framing and the three limits are unchanged.
- Verify: voice 0 errors; refs 0 missing/0 unused; claims 0 unmatched; check => PASS; synced.
