from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable
import fitz
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

Progress = Callable[[str, int], None]

@dataclass
class OMRResult:
    midi_path: Path | None
    diagnostics: list[str] = field(default_factory=list)
    passed: bool = False

class ChoirOMREngine:
    VERSION = "0.1.0"

    def process(self, source: Path, output: Path, progress: Progress) -> OMRResult:
        diagnostics: list[str] = []
        progress("Reading document", 10)
        doc = fitz.open(source)
        if doc.page_count < 1:
            return OMRResult(None, ["Document contains no pages."], False)

        progress("Detecting systems", 25)
        # Recognition stages intentionally remain explicit. We do not fabricate
        # notes when the recognizer has not established them.
        pages = [page.get_text("dict") for page in doc]

        progress("Reconstructing staves", 40)
        diagnostics.append(f"Loaded {len(pages)} page(s).")

        progress("Reading musical events", 60)
        events = self._recognize_written_events(doc, diagnostics)

        progress("Validating measures", 80)
        if not events:
            diagnostics.append(
                "No validated written musical events were recognized. "
                "MIDI generation blocked: no downstream patching is permitted."
            )
            return OMRResult(None, diagnostics, False)

        progress("Compiling MIDI", 92)
        self._compile_midi(events, output)
        progress("Complete", 100)
        return OMRResult(output, diagnostics, True)

    def _recognize_written_events(self, doc, diagnostics):
        # This is the engine boundary we improve version by version.
        # Returning [] is deliberate until recognition evidence is sufficient.
        return []

    def _compile_midi(self, events, output: Path):
        midi = MidiFile(ticks_per_beat=480)
        track = MidiTrack()
        midi.tracks.append(track)
        track.append(MetaMessage("set_tempo", tempo=bpm2tempo(84), time=0))
        for event in events:
            track.append(Message("note_on", note=event["midi"], velocity=64, time=event["delta"]))
            track.append(Message("note_off", note=event["midi"], velocity=0, time=event["duration"]))
        midi.save(output)
