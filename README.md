# subthreshold-worlds

How many grains make a heap? The number was never the point. This paper reads the heap as one instance of a wide architecture: a latent state accumulates small changes (x_{t+1} = F(x_t, u_t)) while a coarse readout classifying it stays fixed (y_t = R(x_t)), so that R(x_{t+1}) = R(x_t) though x_{t+1} != x_t, until eventually the readout flips. The paradox is the confusion of readout-invariance with state-invariance — of a non-transitive tolerance relation with a transitive equivalence relation. Four claims are grounded in a reproducible simulation: (1) a population of leaky integrators holds the accumulated count (linear decode R^2 = 1.0) while the thresholded readout is silent for 37 steps and carries zero information — a subthreshold input is nothing only to the spike that has not fired; (2) indistinguishability holds for every adjacent pair (rate 1.0) yet its transitive closure merges 1000 distinct states into 1 class, and 75% of chained triples fail transitivity; (3) a soft threshold makes local tolerance and global transition coexist (largest per-grain change 0.0062, total 1.0); (4) a bistable latent state driven across a fold gives the readout no warning until the jump, while variance rises ~15x, autocorrelation climbs 0.9 -> 0.99, and a reservoir alarms 198 steps early. Spans sorites/vagueness, subitization/categorical perception, synaptic summation, reservoir computing, and multicellularity. Bounded: it does not name a grain number, does not claim neurons are heaps or cells are reservoirs, and takes the sheaf-theoretic reading only as far as "local readouts need not glue into one global predicate." Ships a runnable simulation whose output carries every modelled number.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run
`papers build subthreshold-worlds`.

## Simulation

```bash
cd simulation && uv run run_all.py   # -> output/results.json, output/figures/
```

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace
docs for the research and writing pipelines.
