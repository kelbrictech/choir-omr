from dataclasses import dataclass
from fractions import Fraction

class RhythmAmbiguity(ValueError):
    pass

@dataclass(frozen=True)
class RhythmEvidence:
    filled_notehead: bool
    has_stem: bool
    flag_count: int = 0
    beam_count: int = 0
    dot_count: int = 0

def classify_duration(e: RhythmEvidence) -> Fraction:
    """Return duration in quarter-note units from structural notation evidence.

    Flags and beams are alternate encodings of subdivision depth. A note must
    not simultaneously derive its depth from both. Ambiguous/incomplete
    evidence is rejected rather than guessed.
    """
    if e.flag_count < 0 or e.beam_count < 0 or e.dot_count < 0:
        raise RhythmAmbiguity("negative rhythmic evidence")
    if e.flag_count and e.beam_count:
        raise RhythmAmbiguity("note cannot be classified from flag and beam evidence simultaneously")
    if not e.has_stem:
        raise RhythmAmbiguity("stemless duration requires a separate whole-note classifier")

    depth = e.flag_count or e.beam_count
    if e.filled_notehead:
        base = Fraction(1, 2 ** depth)  # quarter=1, eighth=1/2, sixteenth=1/4
    else:
        if depth:
            raise RhythmAmbiguity("open notehead with flag/beam needs explicit validation")
        base = Fraction(2, 1)  # half note

    value = base
    addition = base
    for _ in range(e.dot_count):
        addition /= 2
        value += addition
    return value
