"""Subthreshold Worlds — latent accumulation under a coarse-grained readout.

One architecture runs through sorites heaps, synaptic summation, reservoir
computation, and multicellular transitions:

    x_{t+1} = F(x_t, u_t)        (a latent state accumulates small inputs)
    y_t     = R(x_t)             (a coarse readout classifies it)

with the sorites condition that for many steps the state moves while the readout
does not, R(x_{t+1}) = R(x_t) though x_{t+1} != x_t, until eventually R flips.
The paradox is the confusion of readout-invariance with state-invariance, i.e.
of a non-transitive tolerance relation with a transitive equivalence relation.

Four studies, one architecture:
  1. subthreshold_summation   a population of leaky integrators holds the
                              accumulated count (a linear decoder recovers it,
                              R^2 ~ 1) while the thresholded readout is silent,
                              carrying zero information about how much arrived
  2. nontransitive_relation   local indistinguishability holds for every
                              adjacent pair yet its transitive closure collapses
                              a thousand distinct states into one class
  3. tolerance_vs_transition  a soft threshold: the per-step change in category
                              probability is tiny while the total change is ~1
  4. critical_transition      slow accumulation drives a bistable latent state
                              across a fold; the readout gives no warning, but
                              critical slowing down (rising autocorrelation and
                              variance) and a reservoir both flag it in advance

Run `uv run run_all.py`. Seeded (SEED) so every number is reproducible.
"""
from __future__ import annotations

import numpy as np

SEED = 20260701


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


# --------------------------------------------------------------------------- #
# Study 1 — subthreshold summation: the latent state holds what the readout    #
# discards                                                                     #
# --------------------------------------------------------------------------- #
def subthreshold_summation(rng) -> dict:
    """A population of leaky integrators driven by a stream of small inputs.
    The population state linearly encodes the accumulated input count; the
    thresholded (spike / heap) readout stays silent for a long window, so it
    carries no information about how much has accumulated."""
    M, T = 60, 400
    leaks = rng.uniform(0.90, 0.995, M)          # heterogeneous time constants
    w_in = rng.uniform(0.5, 1.5, M)
    inp = np.full(T, 0.05)                        # one small "grain" per step
    count = np.cumsum(np.ones(T))                 # true accumulated number
    X = np.zeros((T, M))
    x = np.zeros(M)
    for t in range(T):
        x = leaks * x + w_in * inp[t]
        X[t] = x
    # coarse readout: a spike/heap when the population sum crosses a threshold
    pop = X.sum(1)
    theta = 0.6 * pop.max()
    y = (pop > theta).astype(int)
    first_cross = int(np.argmax(y == 1))         # end of the subthreshold window

    # linear decode of the accumulated count from the latent population state
    Phi = np.hstack([X, np.ones((T, 1))])
    W, *_ = np.linalg.lstsq(Phi, count, rcond=None)
    pred = Phi @ W
    ss_res = ((count - pred) ** 2).sum()
    ss_tot = ((count - count.mean()) ** 2).sum()
    decode_r2 = float(1 - ss_res / ss_tot)

    # over the subthreshold window the readout is constant -> zero information
    win = slice(0, first_cross)
    readout_var = float(np.var(y[win]))
    latent_change = float(np.mean(np.abs(np.diff(pop[win]))))
    count_grew = float(count[first_cross - 1] / count[0])

    return dict(
        M=M, T=T, subthreshold_window=first_cross,
        decode_r2=decode_r2, readout_var_in_window=readout_var,
        mean_latent_step=latent_change, count_grew_factor=count_grew,
        r_decode_r2=round(decode_r2, 3),
        r_window=first_cross,
        r_count_grew=int(round(count_grew)),
    )


# --------------------------------------------------------------------------- #
# Study 2 — non-transitive indistinguishability                                #
# --------------------------------------------------------------------------- #
def nontransitive_relation() -> dict:
    """phi_n = n for n = 1..N; n ~ m iff |phi_n - phi_m| < eps (a JND). Every
    adjacent pair is indistinguishable, yet the transitive closure merges all N
    states into a single class while they are in truth all distinct."""
    N, eps = 1000, 3
    idx = np.arange(1, N + 1)

    adjacent_indist = float(np.mean(np.abs(np.diff(idx)) < eps))   # = 1.0
    endpoint_gap = float(idx[-1] - idx[0])
    endpoint_ratio = endpoint_gap / eps
    # transitive closure of a threshold relation on a line = one interval-connected class
    closure_classes = 1 if (np.diff(idx) < eps).all() else int((np.diff(idx) >= eps).sum() + 1)
    true_classes = N

    # intransitivity: among chained triples i~j, j~k, the fraction with not(i~k)
    chained = 0
    intransitive = 0
    for d1 in range(1, eps):
        for d2 in range(1, eps):
            # i, i+d1, i+d1+d2 with d1,d2 < eps
            chained += (N - d1 - d2)
            if d1 + d2 >= eps:
                intransitive += (N - d1 - d2)
    intransitive_frac = intransitive / chained

    return dict(
        N=N, eps=eps,
        adjacent_indistinguishable=adjacent_indist,
        endpoint_gap=endpoint_gap, endpoint_ratio=endpoint_ratio,
        closure_classes=closure_classes, true_classes=true_classes,
        intransitive_frac=intransitive_frac,
        r_adjacent=round(adjacent_indist, 2),
        r_endpoint_ratio=round(endpoint_ratio, 0),
        r_intransitive_pct=round(100 * intransitive_frac),
    )


# --------------------------------------------------------------------------- #
# Study 3 — local tolerance and global transition coexist                      #
# --------------------------------------------------------------------------- #
def tolerance_vs_transition() -> dict:
    """P(heap | n) = sigmoid((n - theta)/tau). The largest single-grain change
    in category probability is tiny; the total change across the range is ~1."""
    N = 2000
    n = np.arange(1, N + 1)
    theta = N / 2

    def profile(tau):
        P = _sigmoid((n - theta) / tau)
        dP = np.abs(np.diff(P))
        borderline = int(np.sum((P > 0.1) & (P < 0.9)))
        return dict(delta_max=float(dP.max()), total=float(P[-1] - P[0]),
                    borderline_width=borderline)

    tight, loose = profile(40.0), profile(160.0)
    ratio = tight["total"] / tight["delta_max"]      # ~ number of effective steps

    return dict(
        N=N, tight=tight, loose=loose,
        steps_ratio=ratio,
        r_delta_max=round(tight["delta_max"], 4),
        r_total=round(tight["total"], 2),
        r_steps_ratio=int(round(ratio)),
        r_borderline_tight=tight["borderline_width"],
        r_borderline_loose=loose["borderline_width"],
    )


# --------------------------------------------------------------------------- #
# Study 4 — critical transition: no readout warning, but latent forewarning     #
# --------------------------------------------------------------------------- #
def _esn(u, rng, n_res=200, rho=0.9, leak=0.3):
    """Drive an echo-state reservoir with signal u; return states."""
    W = rng.standard_normal((n_res, n_res))
    W *= rho / np.max(np.abs(np.linalg.eigvals(W)))
    w_in = rng.uniform(-0.5, 0.5, n_res)
    R = np.zeros((len(u), n_res))
    r = np.zeros(n_res)
    for t in range(len(u)):
        r = (1 - leak) * r + leak * np.tanh(W @ r + w_in * u[t])
        R[t] = r
    return R


def critical_transition(rng) -> dict:
    """Bistable latent state x' = x - x^3 + c(t), with c(t) slowly ramped past
    the fold at c* = 2/(3 sqrt 3) ~ 0.385. The readout 1[x>0] is flat until the
    jump; rolling autocorrelation and variance rise beforehand (critical slowing
    down), and a reservoir readout predicts the jump ahead of the coarse one."""
    T, dt = 6000, 0.01
    c = np.linspace(-0.6, 0.9, T)
    x = np.zeros(T); x[0] = -1.1
    for t in range(T - 1):
        drift = x[t] - x[t] ** 3 + c[t]
        x[t + 1] = x[t] + dt * drift + np.sqrt(dt) * 0.03 * rng.standard_normal()
    y = (x > 0).astype(int)
    flip = int(np.argmax(y == 1))

    # early-warning indicators on a subsampled series (fine dt oversamples, which
    # saturates the autocorrelation; stride restores a meaningful lag-1 measure)
    stride, w = 25, 40
    xs = x[:flip:stride]
    ns = len(xs)
    ac1 = np.full(ns, np.nan); var = np.full(ns, np.nan)
    for i in range(w, ns):
        seg = xs[i - w:i] - xs[i - w:i].mean()
        var[i] = seg.var()
        ac1[i] = np.corrcoef(seg[:-1], seg[1:])[0, 1]
    base = slice(w, w + 15)
    ac_base = float(np.nanmean(ac1[base])); ac_pre = float(np.nanmean(ac1[ns - 15:ns]))
    var_base = float(np.nanmean(var[base])); var_pre = float(np.nanmean(var[ns - 15:ns]))
    # lead: first subsampled index where variance exceeds 2x its baseline
    lead_i = ns
    for i in range(w, ns):
        if not np.isnan(var[i]) and var[i] > 2 * var_base:
            lead_i = i; break
    lead = int((ns - lead_i) * stride)

    # reservoir readout: predict "flip within next H steps" from the noisy signal
    H = 200
    obs = x + 0.05 * rng.standard_normal(T)      # a noisy observable, not y
    R = _esn(obs, rng)
    warmup = 300
    target = np.array([1.0 if (flip - H) <= t < flip else 0.0 for t in range(T)])
    train = slice(warmup, flip - 1)              # only pre-transition data
    Phi = np.hstack([R[train], np.ones((R[train].shape[0], 1))])
    Wc, *_ = np.linalg.lstsq(Phi, target[train], rcond=None)
    pred = np.hstack([R, np.ones((T, 1))]) @ Wc
    # reservoir alarm lead: first t in the pre-window where pred crosses 0.5
    alarm = flip
    for t in range(warmup, flip):
        if pred[t] > 0.5:
            alarm = t; break
    reservoir_lead = flip - alarm

    return dict(
        T=T, flip_step=flip, ew_stride=stride,
        ac1_base=ac_base, ac1_pre=ac_pre, var_base=var_base, var_pre=var_pre,
        var_rise_ratio=float(var_pre / var_base),
        readout_warning=0,                       # the coarse readout is flat until the flip
        slowing_lead=lead, reservoir_lead=reservoir_lead,
        r_ac1_base=round(ac_base, 2), r_ac1_pre=round(ac_pre, 2),
        r_var_rise=round(float(var_pre / var_base), 1),
        r_slowing_lead=lead, r_reservoir_lead=reservoir_lead,
    )


def run() -> dict:
    rng = np.random.default_rng(SEED)
    return dict(
        seed=SEED,
        subthreshold_summation=subthreshold_summation(rng),
        nontransitive_relation=nontransitive_relation(),
        tolerance_vs_transition=tolerance_vs_transition(),
        critical_transition=critical_transition(rng),
    )
