import random
import unittest
from unittest.mock import patch

from code_duel.engine import Game
from code_duel.models import Difficulty, LogicError
from code_duel.rules import ALL_CODES, score, validate
from code_duel.simulation import simulate
from code_duel.solver import Solver
from code_duel.strategies import choose


class RulesTests(unittest.TestCase):
    def test_examples(self):
        for secret, guess, expected in [
            ("1234", "1234", 4),
            ("1234", "4321", 0),
            ("6289", "1234", 1),
            ("1122", "1212", 2),
            ("0000", "1111", 0),
            ("0000", "0000", 4),
            ("0037", "0038", 3),
        ]:
            with self.subTest(secret=secret, guess=guess):
                self.assertEqual(score(secret, guess), expected)

    def test_invalid(self):
        for value in [1234, "", "123", "12345", "１２３４", "١٢٣٤", "12 4", None]:
            with self.assertRaises(ValueError):
                validate(value)

    def test_universe(self):
        self.assertEqual(len(set(ALL_CODES)), 10000)
        self.assertEqual(ALL_CODES[0], "0000")


class SolverTests(unittest.TestCase):
    def test_zero_and_multiple_history(self):
        solver = Solver()
        solver.observe("1234", 0)
        self.assertNotIn("6289", solver.candidates)
        solver.observe("0000", 1)
        self.assertTrue(
            all(
                all(score(c, h.guess) == h.feedback for h in solver.history)
                for c in solver.candidates
            )
        )
        self.assertIn("2105", solver.candidates)  # 1 and 2 still allowed elsewhere

    def test_truth_survives_random_histories(self):
        rng = random.Random(10)
        for secret in rng.sample(ALL_CODES, 100):
            solver = Solver()
            for _ in range(4):
                guess = rng.choice(solver.candidates)
                solver.observe(guess, score(secret, guess))
                self.assertIn(secret, solver.candidates)
                if guess == secret:
                    break

    def test_transactional_impossible_feedback(self):
        solver = Solver()
        solver.observe("0000", 4)
        before = (solver.history, solver.candidates)
        with self.assertRaises(LogicError):
            solver.observe("1111", 0)
        self.assertEqual(before, (solver.history, solver.candidates))

    def test_contradiction_does_not_commit(self):
        solver = Solver()
        solver.observe("0000", 0)
        solver.observe("1111", 3)
        before = (solver.history, solver.candidates)
        guess = solver.candidates[0]
        # An all-correct answer is always possible; choose an impossible bin instead.
        possible = {score(c, guess) for c in solver.candidates}
        impossible = next(i for i in range(5) if i not in possible)
        with self.assertRaises(LogicError):
            solver.observe(guess, impossible)
        self.assertEqual(before, (solver.history, solver.candidates))


class StrategyTests(unittest.TestCase):
    def test_all_difficulties_legal_and_converge(self):
        for level in Difficulty:
            solver = Solver()
            rng = random.Random(123)
            for _ in range(40):
                guess = choose(solver, level, rng)
                self.assertIn(guess, solver.candidates)
                self.assertNotIn(guess, [h.guess for h in solver.history])
                self.assertTrue(all(score(guess, h.guess) == h.feedback for h in solver.history))
                solver.observe(guess, score("0037", guess))
                if guess == "0037":
                    break
            else:
                self.fail("did not converge")

    def test_singleton_and_empty(self):
        for level in Difficulty:
            solver = Solver()
            solver._candidates = ("0037",)
            self.assertEqual(choose(solver, level), "0037")
            solver._candidates = ()
            with self.assertRaises(LogicError):
                choose(solver, level)

    def test_revalidate_corrupted_candidates(self):
        solver = Solver()
        solver.observe("1234", 0)
        solver._candidates = ("6289",)
        for level in Difficulty:
            with self.assertRaises(LogicError):
                choose(solver, level)

    def test_secret_is_not_in_interface(self):
        import inspect

        self.assertEqual(list(inspect.signature(Solver).parameters), ["length"])
        self.assertNotIn("secret", inspect.signature(choose).parameters)
        self.assertFalse(any("secret" in key for key in vars(Solver())))

    def test_simulation_reproducible(self):
        a = simulate("0007", "easy", 7)
        b = simulate("0007", "easy", 7)
        self.assertEqual(
            [(h["guess"], h["feedback"], h["candidates"]) for h in a["history"]],
            [(h["guess"], h["feedback"], h["candidates"]) for h in b["history"]],
        )


class EngineTests(unittest.TestCase):
    def test_outcomes_and_fixed_secrets(self):
        for guess, ai_guess, outcome in [
            ("9999", "1234", "player"),
            ("1111", "0037", "ai"),
            ("9999", "0037", "draw"),
        ]:
            game = Game("0037", "easy", ai_secret="9999")
            with self.assertRaises(LogicError):
                game.reveal()
            with patch("code_duel.engine.choose", return_value=ai_guess):
                game.play_round(guess)
            self.assertEqual(game.outcome, outcome)
            self.assertEqual(game.reveal(), ("0037", "9999"))
            with self.assertRaises(LogicError):
                game.play_round("0000")

    def test_two_round_history_and_reset(self):
        game = Game("0037", "easy", ai_secret="9999")
        with patch("code_duel.engine.choose", side_effect=["1234", "0037"]):
            game.play_round("1111")
            game.play_round("9999")
        self.assertEqual(game.outcome, "draw")
        self.assertEqual([r.number for r in game.rounds], [1, 2])
        new = Game("0000")
        self.assertEqual(new.rounds, ())
        self.assertEqual(new.candidate_count, 10000)
        with self.assertRaises(AttributeError):
            game.difficulty = Difficulty.HARD

    def test_invalid_input_is_atomic(self):
        game = Game("0037")
        with self.assertRaises(ValueError):
            game.play_round("１２３４")
        self.assertEqual(game.rounds, ())
        self.assertEqual(game.candidate_count, 10000)
        for invalid in ["0", "12345"]:
            with self.assertRaises(ValueError):
                Game(invalid)

    def test_no_secret_crosses_strategy_interface(self):
        game = Game("0037", "easy", ai_secret="9999")

        def inspect_solver(solver, difficulty, rng):
            self.assertFalse(any("secret" in key for key in vars(solver)))
            self.assertEqual(solver.history, ())
            return "1234"

        with patch("code_duel.engine.choose", side_effect=inspect_solver):
            game.play_round("1111")


if __name__ == "__main__":
    unittest.main()
