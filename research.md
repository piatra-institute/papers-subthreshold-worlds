# Research

Findings, tiered by source proximity. See the workspace docs (`papers docs`): research-pipeline.md §2.
T1 primary · T2 authoritative secondary · T3 reference · T4 general web (leads only).
A claim that reaches the paper rests on a T1 or T2 source.

## Findings

Simulation (own computation, T1 — simulation/analyses.py, seeded SEED=20260701):
- [T1] Subthreshold summation: a population of 60 leaky integrators; thresholded readout silent for 37 steps (variance 0) while accumulated count grows 37x; linear decode of the count from the latent state R^2 = 1.0. — §5 (latent holds what the readout discards).
- [T1] Non-transitive indistinguishability: chain of 1000 states, tolerance eps=3; adjacent-indistinguishable rate 1.0; endpoints differ 333x the tolerance; transitive closure = 1 class vs 1000 true; 75% of chained triples intransitive. — §3 (sorites = tolerance treated as equivalence).
- [T1] Soft threshold: P=sigmoid((n-theta)/tau); largest single-grain change 0.0062, total change 1.0 (ratio ~160); borderline width 175 (tight tau) vs 703 (loose tau). — §5 (local tolerance + global transition coexist).
- [T1] Critical transition: bistable x'=x-x^3+c(t) ramped across the fold (c*~0.385); flip at step 4483, readout warning 0; variance rises ~15x, lag-1 autocorrelation 0.9 -> 0.99; critical-slowing lead 1450 steps, reservoir (echo-state) alarm 198 steps ahead. — §7 (latent forewarns, readout silent).

Vagueness / logic (T1/T2):
- [T1] Cobreros, Égré, Ripley & van Rooij (2012, J. Phil. Logic 41:347): strict-tolerant logic. — §3.
- [T1] Dzhafarov & Perry (2014, Atten. Percept. Psychophys. 76:2441): perceptual matching probabilistic; soritical endpoints in the lab. — §3. (Correction: Perry, not a second Dzhafarov.)
- [T2] Williamson (1994), Fine (1975, Synthese 30:265), Raffman (2014): epistemicism / supervaluationism / multiple-range. — §3. SEP sorites (Raffman & Hyde, latest ed.) as background.

Numerical cognition / perception (T1/T2):
- [T2] Hyde (2011, Front. Hum. Neurosci. 5:150); Feigenson, Dehaene & Spelke (2004, TICS 8:307): subitization vs ANS. Nieder & Miller (2004, PNAS 101:7457): numerosity population code. — §4.
- [T2] Harnad (1987); Bonnasse-Gahot & Nadal (2022, Neural Computation 34:437): categorical perception (compression/separation). — §4.

Neuron / reservoir (T1/T2):
- [T1] Hodgkin & Huxley (1952, J. Physiol. 117:500); Burkitt (2006, Biol. Cybern. 95:1): membrane integration / integrate-and-fire. — §5.
- [T1/T2] Jaeger & Haas (2004, Science 304:78); Maass, Natschläger & Markram (2002, Neural Comput. 14:2531, LSM); Lukoševičius & Jaeger (2009, Comput. Sci. Rev. 3:127): reservoir computing / echo-state / liquid state machines. — §6.

Transitions / emergence (T1/T2):
- [T1] Scheffer et al. (2009, Nature 461:53): early-warning signals / critical slowing down. — §7.
- [T2] Szathmáry & Maynard Smith (1995, Nature 374:227); Knoll (2011, Annu. Rev. Earth Planet. Sci. 39:217); Brunet & King (2017, Dev. Cell 43:124): major transitions / multicellularity. — §8.
- [T1] Abramsky & Brandenburger (2011, New J. Phys. 13:113036); Mac Lane & Moerdijk (1992): sheaf-theoretic contextuality / topos machinery. — §8 (local-to-global obstruction).

Verification: 23 candidates verified against journals/arXiv/SEP/DOI; corrections applied (SEP order + edition; Dzhafarov & Perry; Bonnasse-Gahot & Nadal 2022). 0 confabulated (refs MISSING = 0).
