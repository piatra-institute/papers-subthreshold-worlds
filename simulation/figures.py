"""Figures for Subthreshold Worlds."""
from __future__ import annotations

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from analyses import _sigmoid, SEED


def plot_two_containers(results: dict, path: str) -> None:
    """The latent state moves every step while the coarse readout stays flat,
    then flips; and the soft-threshold profile: tiny per-step, total ~ 1."""
    s = results["subthreshold_summation"]
    rng = np.random.default_rng(SEED)
    M, T = s["M"], s["T"]
    leaks = rng.uniform(0.90, 0.995, M); w_in = rng.uniform(0.5, 1.5, M)
    inp = np.full(T, 0.05); X = np.zeros((T, M)); x = np.zeros(M)
    for t in range(T):
        x = leaks * x + w_in * inp[t]; X[t] = x
    pop = X.sum(1); theta = 0.6 * pop.max(); y = (pop > theta).astype(int)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
    ax1.plot(pop / pop.max(), color="#1b3a5b", lw=2, label="latent state (moves every step)")
    ax1.plot(y, color="#c0392b", lw=2, label="coarse readout (flat, then flips)")
    ax1.axvline(s["subthreshold_window"], color="#7f8c8d", ls=":", lw=1)
    ax1.set_xlabel("accumulation step"); ax1.set_ylabel("normalized value")
    ax1.set_title(f"Latent decodable (R^2={s['decode_r2']:.3f}); readout silent "
                  f"{s['subthreshold_window']} steps", fontsize=9.5)
    ax1.legend(fontsize=8)

    t = results["tolerance_vs_transition"]
    N = t["N"]; n = np.arange(1, N + 1); theta2 = N / 2
    for tau, col, lab in ((40.0, "#c0392b", "tight"), (160.0, "#27ae60", "loose")):
        P = _sigmoid((n - theta2) / tau)
        ax2.plot(n, P, color=col, lw=2, label=f"tau={tau:g} ({lab})")
    ax2.set_xlabel("grains n"); ax2.set_ylabel("P(heap | n)")
    ax2.set_title(f"Per-grain change {t['tight']['delta_max']:.4f}, total {t['tight']['total']:.2f}",
                  fontsize=9.5)
    ax2.legend(fontsize=8)

    fig.tight_layout(); fig.savefig(path, dpi=140); plt.close(fig)


def plot_nontransitivity(results: dict, path: str) -> None:
    n = results["nontransitive_relation"]
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.bar(["transitive closure\nof indistinguishability", "true distinct\nstates"],
           [n["closure_classes"], n["true_classes"]],
           color=["#c0392b", "#1b3a5b"])
    ax.set_yscale("log")
    ax.set_ylabel("number of classes (log scale)")
    ax.set_title(f"Sorites collapse: adjacent-indistinguishable {n['adjacent_indistinguishable']:.2f}, "
                 f"\n{n['r_intransitive_pct']}% of chained triples intransitive", fontsize=9.5)
    for i, v in enumerate([n["closure_classes"], n["true_classes"]]):
        ax.annotate(str(v), (i, v), textcoords="offset points", xytext=(0, 4), ha="center")
    fig.tight_layout(); fig.savefig(path, dpi=140); plt.close(fig)


def plot_critical_transition(results: dict, path: str) -> None:
    c = results["critical_transition"]
    rng = np.random.default_rng(SEED)
    # replay the run (consume the earlier draws so the trajectory matches)
    _ = rng.uniform(0.90, 0.995, 60); _ = rng.uniform(0.5, 1.5, 60)  # study 1 draws
    T, dt = c["T"], 0.01
    ctl = np.linspace(-0.6, 0.9, T); x = np.zeros(T); x[0] = -1.1
    for t in range(T - 1):
        x[t + 1] = x[t] + dt * (x[t] - x[t] ** 3 + ctl[t]) + np.sqrt(dt) * 0.03 * rng.standard_normal()
    flip = c["flip_step"]
    stride, w = c["ew_stride"], 40
    xs = x[:flip:stride]; ns = len(xs)
    var = np.full(ns, np.nan)
    for i in range(w, ns):
        seg = xs[i - w:i] - xs[i - w:i].mean(); var[i] = seg.var()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 5.2), sharex=True)
    tt = np.arange(T)
    ax1.plot(tt, x, color="#1b3a5b", lw=0.8, label="latent state x")
    ax1.plot(tt, (x > 0).astype(int), color="#c0392b", lw=1.5, label="coarse readout (no warning)")
    ax1.axvline(flip, color="#2c3e50", ls="--", lw=1)
    ax1.set_ylabel("state / readout"); ax1.legend(fontsize=8, loc="center left")
    ax1.set_title(f"Readout flat until the flip; variance rises {c['var_rise_ratio']:.0f}x, "
                  f"reservoir alarms {c['reservoir_lead']} steps early", fontsize=9.5)

    ax2.plot(np.arange(ns) * stride, var, color="#e67e22", lw=1.5, label="rolling variance (early warning)")
    ax2.axvline(flip, color="#2c3e50", ls="--", lw=1)
    ax2.set_xlabel("step"); ax2.set_ylabel("variance"); ax2.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(path, dpi=140); plt.close(fig)
