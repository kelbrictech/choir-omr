from fractions import Fraction
import pytest
from engine.rhythm import RhythmEvidence, RhythmAmbiguity, classify_duration

def test_filled_stem_no_flag_is_quarter():
    assert classify_duration(RhythmEvidence(True, True)) == Fraction(1, 1)

def test_one_flag_is_eighth():
    assert classify_duration(RhythmEvidence(True, True, flag_count=1)) == Fraction(1, 2)

def test_one_beam_is_eighth():
    assert classify_duration(RhythmEvidence(True, True, beam_count=1)) == Fraction(1, 2)

def test_two_beams_is_sixteenth_not_eighth():
    assert classify_duration(RhythmEvidence(True, True, beam_count=2)) == Fraction(1, 4)

def test_two_flags_is_sixteenth_not_eighth():
    assert classify_duration(RhythmEvidence(True, True, flag_count=2)) == Fraction(1, 4)

def test_dotted_eighth():
    assert classify_duration(RhythmEvidence(True, True, flag_count=1, dot_count=1)) == Fraction(3, 4)

def test_flag_and_beam_conflict_is_not_guessed():
    with pytest.raises(RhythmAmbiguity):
        classify_duration(RhythmEvidence(True, True, flag_count=1, beam_count=1))

def test_missing_stem_is_not_guessed_as_eighth():
    with pytest.raises(RhythmAmbiguity):
        classify_duration(RhythmEvidence(True, False, flag_count=1))
