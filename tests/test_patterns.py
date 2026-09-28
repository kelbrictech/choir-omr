from fractions import Fraction
from engine.patterns import PatternEvent, beat_boundaries, validate_measure_pattern, candidate_fits_measure

E=PatternEvent

def test_three_four_six_eighths_fill_measure():
    r=validate_measure_pattern([E(Fraction(1,2))]*6,3,4)
    assert r.valid and r.total == 3

def test_three_four_quarter_plus_four_eighths():
    assert validate_measure_pattern([E(1),E(Fraction(1,2)),E(Fraction(1,2)),E(Fraction(1,2)),E(Fraction(1,2))],3,4).valid

def test_three_four_dotted_quarter_three_eighths():
    assert validate_measure_pattern([E(Fraction(3,2)),E(Fraction(1,2)),E(Fraction(1,2)),E(Fraction(1,2))],3,4).valid

def test_bad_eighth_as_quarter_breaks_three_four_arithmetic():
    assert not validate_measure_pattern([E(1)]*6,3,4).valid

def test_six_eight_compound_beat_boundaries():
    assert beat_boundaries(6,8) == (Fraction(3,2), Fraction(3,1))

def test_nine_eight_compound_beat_boundaries():
    assert beat_boundaries(9,8) == (Fraction(3,2),Fraction(3,1),Fraction(9,2))

def test_irregular_grouping_can_be_explicit():
    assert beat_boundaries(7,8,(2,3,2)) == (Fraction(1),Fraction(5,2),Fraction(7,2))

def test_pattern_can_reject_wrong_candidate_without_rewriting_it():
    prefix=[E(1),E(1)]
    assert candidate_fits_measure(prefix,Fraction(1),[],3,4)
    assert not candidate_fits_measure(prefix,Fraction(1,2),[],3,4)
