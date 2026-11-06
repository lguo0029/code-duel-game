# Benchmark method and results

| Strategy | Secrets | Mean guesses | Median | P95 | Worst | Invalid | Failed |
|---|---:|---:|---:|---:|---:|---:|---:|
| easy | 10000 | 10.3033 | 11.0 | 13 | 16 | 0 | 0 |
| medium | 10000 | 10.1034 | 10.0 | 12 | 16 | 0 | 0 |
| hard | 10000 | 10.0880 | 10.0 | 12 | 16 | 0 | 0 |

| Seed | Easy mean | Medium mean | Hard mean |
|---|---:|---:|---:|
| 7 | 10.174 | 10.103 | 10.092 |
| 101 | 10.264 | 10.049 | 10.109 |

Fixed parameters are embedded in each report. All 10,000 four-digit codes are distinct;
strategies use the same seeded answer ordering and shared opening-randomization rule.
The secret is only passed to the external score function, never to choose().
Each actual guess is revalidated against the complete history; a repeat or
excluded guess aborts the run. No failure is silently dropped. Full runtime is
25.222 seconds. Decision time includes cached shared-history
lookup; true uncached strategy time is stored in representative traces. No claim
of significant improvement is made: seed 101 reverses Medium/Hard ordering.
The earlier 1000-secret means are historical samples, not full-space estimates.

Reproduction: use README commands. Reports record environment, parameters, sample
size, seeds, failures, outcomes, histograms and conditional candidate trajectories.
Runtime varies with load. Raw compressed CSV preserves all game outcomes.
