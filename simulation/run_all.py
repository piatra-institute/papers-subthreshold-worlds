"""Orchestrator: reproduces every modelled number in the paper.

    cd simulation
    uv run run_all.py

Writes output/results.json and output/figures/. Seeded (analyses.SEED).
"""
from __future__ import annotations

import json
from pathlib import Path

from analyses import run
from figures import (plot_two_containers, plot_nontransitivity,
                     plot_critical_transition)

OUT = Path(__file__).parent / "output"


def main() -> None:
    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    results = run()
    (OUT / "results.json").write_text(json.dumps(results, indent=2))
    plot_two_containers(results, str(OUT / "figures" / "two_containers.png"))
    plot_nontransitivity(results, str(OUT / "figures" / "nontransitivity.png"))
    plot_critical_transition(results, str(OUT / "figures" / "critical_transition.png"))

    s, n = results["subthreshold_summation"], results["nontransitive_relation"]
    t, c = results["tolerance_vs_transition"], results["critical_transition"]
    print("1. SUBTHRESHOLD SUMMATION")
    print(f"   readout silent for              : {s['subthreshold_window']} steps "
          f"(count grew {s['count_grew_factor']:.0f}x)")
    print(f"   latent decode of the count  R^2 : {s['decode_r2']:.3f}  "
          f"(readout variance in window {s['readout_var_in_window']:.3f})")
    print("2. NON-TRANSITIVE INDISTINGUISHABILITY")
    print(f"   adjacent pairs indistinguishable: {n['adjacent_indistinguishable']:.2f}  "
          f"(endpoints differ {n['endpoint_ratio']:.0f}x the tolerance)")
    print(f"   transitive-closure classes      : {n['closure_classes']}  vs  {n['true_classes']} true")
    print(f"   chained triples that are intransitive: {100*n['intransitive_frac']:.0f}%")
    print("3. LOCAL TOLERANCE, GLOBAL TRANSITION")
    print(f"   largest per-grain change in P   : {t['tight']['delta_max']:.4f}")
    print(f"   total change across the range   : {t['tight']['total']:.2f}  "
          f"(ratio {t['steps_ratio']:.0f})")
    print(f"   borderline width  tight / loose : {t['r_borderline_tight']} / {t['r_borderline_loose']} grains")
    print("4. CRITICAL TRANSITION")
    print(f"   flip step                       : {c['flip_step']}  (readout warning: {c['readout_warning']})")
    print(f"   autocorrelation  base -> pre    : {c['ac1_base']:.2f} -> {c['ac1_pre']:.2f}")
    print(f"   variance rise before the flip   : {c['var_rise_ratio']:.0f}x")
    print(f"   lead: slowing / reservoir       : {c['slowing_lead']} / {c['reservoir_lead']} steps")


if __name__ == "__main__":
    main()
