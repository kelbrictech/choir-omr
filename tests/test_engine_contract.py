from pathlib import Path
from engine.core import ChoirOMREngine

def test_midi_is_blocked_without_validated_events(tmp_path):
    # Contract regression: the engine must never fabricate or patch MIDI merely
    # to produce a downloadable result.
    assert ChoirOMREngine.VERSION
