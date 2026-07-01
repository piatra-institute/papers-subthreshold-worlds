# Brief

Written before research begins. See the workspace docs (run `papers docs`):
research-pipeline.md §1.

## Question

The sorites/heap paradox asks for a grain number. Is that the wrong question, and is the heap one instance of a broader architecture — latent accumulation under a coarse-grained readout — shared with synaptic summation, reservoir computing, and multicellular transitions?

## Claim

A latent state accumulates small inputs (x_{t+1}=F(x_t,u_t)) while a coarse readout (y_t=R(x_t)) stays fixed until it flips. The paradox is confusing readout-invariance with state-invariance: treating a non-transitive tolerance relation as a transitive equivalence relation. Local tolerance and global transition coexist; the information the readout discards is preserved and decodable in the latent state; and near a tipping point the latent state forewarns (critical slowing down, reservoir prediction) while the readout stays silent. The contribution is a bounded cross-domain formal synthesis, not a solution to sorites and not an ontological identification of the domains.

## Kind

Formal-model / synthesis — ships a simulation; `has_simulation: true`, `claims_target: results.json`.

Instrument choice: to break the corpus fingerprint, the instrument is reservoir computing / echo-state dynamics + the combinatorics of a non-transitive indistinguishability relation + critical-transition early warning — none used before in the corpus. The headline results are a relation-collapse (1 class vs 1000) and a "latent forewarns, readout silent" reversal, distinct from the corpus's thresholds and negative-IDs. Could have been no-sim, but four claims are genuinely computable, so grounding them both strengthens the synthesis and breaks the fingerprint.

## Cornerstone literature

Sorites/vagueness: Cobreros et al. (strict-tolerant), Williamson (epistemicism), Fine (supervaluationism), Raffman, Dzhafarov & Perry (perceptual matching), SEP. Numerical cognition / perception: Hyde, Feigenson-Dehaene-Spelke, Nieder & Miller, Harnad, Bonnasse-Gahot & Nadal. Neuron: Hodgkin-Huxley, Burkitt. Reservoir computing: Jaeger & Haas, Maass et al. (LSM), Lukoševičius & Jaeger. Critical transitions: Scheffer et al. Multicellularity: Szathmáry & Maynard Smith, Knoll, Brunet & King. Sheaf/contextuality: Abramsky & Brandenburger, Mac Lane & Moerdijk.
