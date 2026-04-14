from __future__ import annotations

from dataclasses import dataclass, field

from .validate import (
    WORD_LENGTH,
    Feedback,
    compute_feedback,
    validate_guess,
)


class GameOverError(RuntimeError):
    pass


@dataclass
class GuessResult:
    feedback: Feedback
    solved: bool
    guess_count: int


@dataclass
class GameState:
    target: str
    max_guesses: int = 6
    guesses: list[str] = field(default_factory=list)
    solved: bool = False

    def __post_init__(self) -> None:
        self.target = self.target.strip().upper()
        if len(self.target) != WORD_LENGTH or not self.target.isalpha():
            raise ValueError(
                f"target must be {WORD_LENGTH} letters (got {self.target!r})"
            )

    @property
    def guess_count(self) -> int:
        return len(self.guesses)

    @property
    def over(self) -> bool:
        return self.solved or self.guess_count >= self.max_guesses

    def guess(self, guess: str) -> GuessResult:
        if self.over:
            raise GameOverError("game is already over")
        g = validate_guess(guess)
        feedback = compute_feedback(g, self.target)
        self.guesses.append(g)
        if all(f == "hit" for f in feedback):
            self.solved = True
        return GuessResult(
            feedback=feedback,
            solved=self.solved,
            guess_count=self.guess_count,
        )
