import pytest

from game.validate import (
    InvalidGuessError,
    compute_feedback,
    is_valid_guess,
    normalize,
    validate_guess,
)


class TestNormalize:
    def test_uppercases(self):
        assert normalize("hello") == "HELLO"

    def test_strips_whitespace(self):
        assert normalize("  hello  ") == "HELLO"

    def test_already_uppercase(self):
        assert normalize("HELLO") == "HELLO"


class TestIsValidGuess:
    def test_accepts_five_letters(self):
        assert is_valid_guess("HELLO")

    def test_accepts_lowercase(self):
        assert is_valid_guess("hello")

    def test_rejects_four_letters(self):
        assert not is_valid_guess("HELL")

    def test_rejects_six_letters(self):
        assert not is_valid_guess("HELLOO")

    def test_rejects_empty(self):
        assert not is_valid_guess("")

    def test_rejects_digits(self):
        assert not is_valid_guess("HELL0")

    def test_rejects_symbols(self):
        assert not is_valid_guess("HELL!")

    def test_rejects_interior_space(self):
        assert not is_valid_guess("HEL O")


class TestValidateGuess:
    def test_returns_normalized(self):
        assert validate_guess("hello") == "HELLO"

    def test_raises_on_short(self):
        with pytest.raises(InvalidGuessError):
            validate_guess("HELL")

    def test_raises_on_digits(self):
        with pytest.raises(InvalidGuessError):
            validate_guess("HELL0")

    def test_raises_on_empty(self):
        with pytest.raises(InvalidGuessError):
            validate_guess("")


class TestComputeFeedback:
    def test_all_hit(self):
        assert compute_feedback("HELLO", "HELLO") == ["hit"] * 5

    def test_all_miss(self):
        assert compute_feedback("QRSTU", "VWXYZ") == ["miss"] * 5

    def test_all_present(self):
        # Every letter appears in HELLO but none at its own position.
        assert compute_feedback("ELHOL", "HELLO") == ["present"] * 5

    def test_mixed_hit_present_miss(self):
        assert compute_feedback("HELOW", "HELLO") == [
            "hit",
            "hit",
            "hit",
            "present",
            "miss",
        ]

    def test_duplicate_guess_one_present_one_miss(self):
        # target APPLE, guess PAPPY: middle P hits, first P is present,
        # trailing P has no remaining target P to match → miss.
        assert compute_feedback("PAPPY", "APPLE") == [
            "present",
            "present",
            "hit",
            "miss",
            "miss",
        ]

    def test_duplicate_target_one_hit_one_present(self):
        # target LEVEL, guess SPEED: second E hits, first E matches the
        # other target E as present.
        assert compute_feedback("SPEED", "LEVEL") == [
            "miss",
            "miss",
            "present",
            "hit",
            "miss",
        ]

    def test_rejects_wrong_length(self):
        with pytest.raises(ValueError):
            compute_feedback("HELL", "HELLO")
        with pytest.raises(ValueError):
            compute_feedback("HELLO", "HELL")
