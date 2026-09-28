from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

@dataclass(frozen=True)
class PatternEvent:
    duration: Fraction
    kind: str = "note"

@dataclass(frozen=True)
class PatternCheck:
    valid: bool
    total: Fraction
    expected: Fraction
    beat_boundaries: tuple[Fraction, ...]

def measure_length(numerator: int, denominator: int) -> Fraction:
    """Measure length in quarter-note units."""
    return Fraction(numerator * 4, denominator)

def default_beat_groups(numerator: int, denominator: int) -> tuple[int, ...]:
    """Conservative metrical grouping used as validation context, not symbol truth."""
    if denominator == 8 and numerator > 3 and numerator % 3 == 0:
        return tuple(3 for _ in range(numerator // 3))
    return tuple(1 for _ in range(numerator))

def beat_boundaries(numerator: int, denominator: int, groups: Sequence[int] | None = None):
    groups = tuple(groups or default_beat_groups(numerator, denominator))
    unit = Fraction(4, denominator)
    expected_units = numerator
    if sum(groups) != expected_units:
        raise ValueError("beat groups must fill the time signature")
    pos = Fraction(0)
    out = []
    for group in groups:
        pos += group * unit
        out.append(pos)
    return tuple(out)

def validate_measure_pattern(events: Sequence[PatternEvent], numerator: int, denominator: int,
                             groups: Sequence[int] | None = None) -> PatternCheck:
    """Validate rhythmic arithmetic against meter.

    Pattern context can reject an impossible recognition, but must not silently
    rewrite a visually recognized duration. That repair belongs upstream.
    """
    total = sum((e.duration for e in events), Fraction(0))
    expected = measure_length(numerator, denominator)
    return PatternCheck(total == expected, total, expected,
                        beat_boundaries(numerator, denominator, groups))

def candidate_fits_measure(prefix: Sequence[PatternEvent], candidate: Fraction,
                           suffix: Sequence[PatternEvent], numerator: int, denominator: int) -> bool:
    events = [*prefix, PatternEvent(candidate), *suffix]
    return validate_measure_pattern(events, numerator, denominator).valid
