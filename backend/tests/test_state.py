import pytest

from game.state import GameOverError, GameState
from game.validate import InvalidGuessError


class TestGameStateInit:
    def test_normalizes_target(self):
        gs = GameState(target="hello")
        assert gs.target == "HELLO"

    def test_strips_target(self):
        gs = GameState(target="  hello  ")
        assert gs.target == "HELLO"

    def test_rejects_short_target(self):
        with pytest.raises(ValueError):
            GameState(target="HELL")

    def test_rejects_non_alpha_target(self):
        with pytest.raises(ValueError):
            GameState(target="HELL0")

    def test_new_game_state(self):
        gs = GameState(target="HELLO")
        assert gs.guess_count == 0
        assert not gs.solved
        assert not gs.over


class TestGameStateGuess:
    def test_correct_guess_solves(self):
        gs = GameState(target="HELLO")
        result = gs.guess("hello")
        assert result.feedback == ["hit"] * 5
        assert result.solved
        assert result.guess_count == 1
        assert gs.solved
        assert gs.over

    def test_wrong_guess_increments_counter(self):
        gs = GameState(target="HELLO")
        result = gs.guess("WORLD")
        assert not result.solved
        assert result.guess_count == 1
        assert not gs.solved
        assert not gs.over

    def test_invalid_guess_raises_and_preserves_state(self):
        gs = GameState(target="HELLO")
        with pytest.raises(InvalidGuessError):
            gs.guess("HI")
        assert gs.guess_count == 0

    def test_max_guesses_ends_game_unsolved(self):
        gs = GameState(target="HELLO", max_guesses=3)
        gs.guess("APPLE")
        gs.guess("WORLD")
        gs.guess("FUDGE")
        assert gs.over
        assert not gs.solved
        assert gs.guess_count == 3

    def test_guess_after_loss_raises(self):
        gs = GameState(target="HELLO", max_guesses=1)
        gs.guess("WORLD")
        with pytest.raises(GameOverError):
            gs.guess("APPLE")

    def test_guess_after_solve_raises(self):
        gs = GameState(target="HELLO")
        gs.guess("HELLO")
        with pytest.raises(GameOverError):
            gs.guess("WORLD")

    def test_history_preserved(self):
        gs = GameState(target="HELLO")
        gs.guess("APPLE")
        gs.guess("WORLD")
        assert gs.guesses == ["APPLE", "WORLD"]
