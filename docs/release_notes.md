# v0.1.0 — portfolio prerelease

- Reconstructed automatic-feedback four-digit human/AI duel.
- English / Simplified Chinese setup, gameplay, errors and results.
- Legal candidate-only random, heuristic and entropy/Minimax strategies.
- Fixed private secrets and simultaneous automatic settlement.
- Real benchmark reports and Matplotlib charts, tests, packaging and CI definitions.
- Local macOS Python 3.14.6 + Tk 8.6 validation; 22 tests passed and real-window integration passed.

Install Python 3.11+ with Tk, then `pip install -e .` and `python main.py`.
Development commands are in the README. Linux/Windows validation depends on the
actual Actions run; do not infer it from local results.

Limitations: native UI screenshots could not be captured. This is an explicitly reconstructed version; Hard has only a small, seed-dependent advantage.
