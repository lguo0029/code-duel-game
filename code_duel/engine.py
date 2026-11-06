"""Reconstructed automatic-feedback game; secrets never cross into the strategy API."""

import random

from .models import DecisionInfo, Difficulty, LogicError, Round
from .rules import ALL_CODES, score, validate
from .solver import Solver
from .strategies import choose


class Game:
    def __init__(
        self,
        player_secret: str,
        difficulty: str = "medium",
        *,
        seed: int | None = None,
        ai_secret: str | None = None,
    ):
        self.__player_secret = validate(player_secret)
        self.__rng = random.Random(seed)
        self.__ai_secret = (
            validate(ai_secret) if ai_secret is not None else self.__rng.choice(ALL_CODES)
        )
        self.__difficulty = Difficulty(difficulty)
        self.__solver = Solver(4)
        self.__rounds: tuple[Round, ...] = ()
        self.__outcome: str | None = None

    @property
    def length(self) -> int:
        return 4

    @property
    def difficulty(self) -> Difficulty:
        return self.__difficulty

    @property
    def rounds(self) -> tuple[Round, ...]:
        return self.__rounds

    @property
    def outcome(self) -> str | None:
        return self.__outcome

    @property
    def candidate_count(self) -> int:
        return len(self.__solver.candidates)

    @property
    def decision(self) -> DecisionInfo | None:
        return getattr(self.__solver, "last_decision", None)

    def play_round(self, player_guess: str) -> Round:
        """Lock both guesses, score both, then decide win/draw atomically."""
        if self.outcome is not None:
            raise LogicError("The game has ended.")
        validate(player_guess)
        ai_guess = choose(self.__solver, self.difficulty, self.__rng)
        self.__solver.check(ai_guess)
        player_score = score(self.__ai_secret, player_guess)
        ai_score = score(self.__player_secret, ai_guess)
        self.__solver.observe(ai_guess, ai_score)
        record = Round(
            len(self.rounds) + 1,
            player_guess,
            player_score,
            ai_guess,
            ai_score,
            self.candidate_count,
        )
        self.__rounds += (record,)
        if player_score == ai_score == 4:
            self.__outcome = "draw"
        elif player_score == 4:
            self.__outcome = "player"
        elif ai_score == 4:
            self.__outcome = "ai"
        return record

    def reveal(self) -> tuple[str, str]:
        if self.outcome is None:
            raise LogicError("The AI secret is hidden until the game ends.")
        return self.__player_secret, self.__ai_secret
