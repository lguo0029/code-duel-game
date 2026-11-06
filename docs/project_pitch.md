# Project pitch

## 30 seconds

CodeDuel is a bilingual Python desktop game where a person and a computer try to break each other’s fixed four-digit secret. I separated the game engine from three search strategies and validated every AI guess against the complete feedback history. I also tested every four-digit answer and reported the small, seed-dependent differences between the strategies.

## 90 seconds

The application is a complete person-versus-computer duel, not two people sharing a keyboard. Both sides choose guesses before the engine scores the round, so a human success does not unfairly remove the AI’s opportunity to draw. Easy chooses a random legal candidate, Medium estimates expected remaining candidates, and Hard maximizes entropy with a Minimax tie-break. I restrict every AI action to a possible answer under all previous clues. The strategy receives a solver state, never the human secret. I validated the full four-digit space for each strategy: thirty thousand completed runs with no detected illegal guess. The means were around ten guesses, with only a small advantage for the more expensive strategies. Another seed reversed Medium and Hard, so I do not claim universal superiority. The UI supports English and Chinese, and reasoning happens off the Tk thread. The original snapshot was unavailable, so this edition is explicitly documented as a reconstruction.

## Three-minute technical explanation

I start with the scoring invariant: only equal digits at equal positions count. There is no misplaced-digit credit. Codes remain strings, so leading zeros and repetitions require no special conversion. All components call the same scorer, which prevents the game, simulation and strategy from drifting into different rules.

The solver maintains the complete legal candidate set. A candidate must reproduce every earlier feedback count. It is not enough to filter on the last clue, and it is not legitimate in this edition to make an information-gathering guess that cannot be the answer. Before formal submission I run the history check again and reject repeated actions. The engine owns both secrets and provides only observations to the strategy. It locks the guesses and settles both scores together, making the same-round draw a state-machine requirement rather than a UI accident.

The three policies expose a useful algorithm tradeoff. Random legal choice is inexpensive. Medium estimates the expected bucket size, sum of squared bucket sizes divided by the sample count. Hard estimates Shannon entropy and uses the largest bucket for near ties. Entropy optimizes average information while Minimax protects a worst branch; neither proves optimal total game depth. Initial guesses are distributionally equivalent, so I avoid scoring them unnecessarily.

I measured all ten thousand answers for each policy and additional seeds. The small differences, and one reversed Medium/Hard ordering, are as important as the best mean. Cache-aware timing cannot be marketed as cold-start latency. Tests, full-space simulation, real-window flows and clean installs cover different failure modes. The remaining work is stronger policy evaluation and presentation, not adding an irrelevant neural model.

## Three hardest problems

1. Enforcing all historical constraints rather than just the latest clue.
2. Settling simultaneous guesses without skipping a valid draw.
3. Measuring small heuristic differences without overstating their significance.

## Representative debugging case

When timing diagnostics were added to simulation histories, the old reproducibility
test compared complete dictionaries, including wall-clock times, and failed. I
fixed the test to compare semantic records (guess, feedback, candidates), leaving
runtime measurements explicitly nondeterministic. This was a test-contract bug,
not evidence of nondeterministic game rules. The failing run was not reported as
a passing result; the final suites were rerun after the correction.

## Optimization evidence

The existing implementation already cached shared-history decisions and avoided
initial distribution evaluation by symmetry. I preserved those mechanisms and
remeasured them rather than inventing an unavailable before/after comparison.
Hard still has a larger sampling cost. There is no justified quantified speedup
against an uncached baseline in this release.

## Next steps

More randomized policies and uncertainty estimates, cold-start latency measurements, persistent match statistics and live language switching.
