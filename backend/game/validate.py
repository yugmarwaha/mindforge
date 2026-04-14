from __future__ import annotations

WORD_LENGTH = 5

Feedback = list[str]


class InvalidGuessError(ValueError):
    pass


def normalize(guess: str) -> str:
    return guess.strip().upper()


def is_valid_guess(guess: str) -> bool:
    g = normalize(guess)
    return len(g) == WORD_LENGTH and g.isascii() and g.isalpha()


def validate_guess(guess: str) -> str:
    g = normalize(guess)
    if not is_valid_guess(g):
        raise InvalidGuessError(
            f"guess must be {WORD_LENGTH} letters A-Z (got {guess!r})"
        )
    return g


def compute_feedback(guess: str, target: str) -> Feedback:
    """Duplicate letters: exact matches consume target positions before
    remaining letters are checked for 'present'."""
    if len(guess) != WORD_LENGTH or len(target) != WORD_LENGTH:
        raise ValueError("guess and target must both be 5 letters")

    feedback: Feedback = ["miss"] * WORD_LENGTH
    target_remaining = list(target)

    for i, ch in enumerate(guess):
        if ch == target[i]:
            feedback[i] = "hit"
            target_remaining[i] = ""

    for i, ch in enumerate(guess):
        if feedback[i] == "hit":
            continue
        if ch in target_remaining:
            feedback[i] = "present"
            target_remaining[target_remaining.index(ch)] = ""

    return feedback
