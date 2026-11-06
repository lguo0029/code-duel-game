# Technical interview notes

## Candidate filtering and correctness

`code_duel/rules.py::score` is the only positional scorer. `solver.py::observe`
forms an immutable proposed history and checks every clue before committing.
The regression 1234 -> 0 must exclude 6289 because its second position matches.
Keeping only the most recent clue would be unsound. Enumerating 10,000 strings
is tractable, preserves zeros and makes exact checking straightforward.

## Entropy versus Minimax

`strategies.py::choose` partitions answer samples by feedback k. With bucket
probabilities p_k, H = -sum(p_k log2 p_k). The expected remaining-size heuristic
is sum(b_k^2)/N. Entropy rewards average information; Minimax minimizes max b_k
and protects against the worst next outcome. Hard first maximizes entropy, then
uses a 0.02-bit near-tie band to select the smallest worst bucket. Restricting
all guesses to valid candidates sacrifices unrestricted probing but makes every
AI guess explainable from prior clues. This is not a global optimality proof.

## Why Hard can lose to Easy

A random choice can hit the answer immediately. Even in expectation, one-step
entropy on a finite sample does not optimize total solution depth. The full-space
seed-42 means were 10.3033, 10.1034 and 10.0880. On a 1000-secret seed-101 sample,
Medium averaged 10.049 while Hard averaged 10.109. This is direct evidence that
the stronger-looking heuristic is not universally better. The larger sampling
budget also costs more. Do not pitch a significant improvement.

## Preventing cheating and handling state

`engine.py::Game` privately owns fixed secrets; `choose(Solver, difficulty, rng)`
receives neither the engine nor a secret. The engine validates the submitted AI
guess again, locks both guesses, scores both and only then decides the outcome.
The draw test specifically verifies that a human success cannot skip the AI turn.
Invalid human input occurs before mutation. Finished games reject further rounds;
a new Game resets all state. Private attributes are a design boundary, not a
security sandbox against Python reflection.

## GUI responsiveness and observability

`gui.py::launch` runs operations on a worker; only `poll` touches Tk. Buttons and
input are disabled while busy. A queue delivers results or exceptions. Diagnostics
come from `DecisionInfo`, with None for unevaluated entropy; an Easy decision never
gets a fabricated entropy explanation. Candidate curves use exact counts.

## Verification and provenance

22 tests plus parameterized subtests, desktop integration in two languages,
clean-wheel installation and the full 30,000-run experiment cover complementary
layers. The automatic engine was reconstructed from the available later edition;
`docs/provenance.md` explicitly records this rather than claiming original recovery.
The CI matrix is evidence only after real jobs finish.
