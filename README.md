# Choir OMR

A choir-specialist Optical Music Recognition engine.

## Product contract

The engine reads a score and produces MIDI. MIDI is a downstream test artifact: corrections belong in the OMR engine, never as post-processing patches to MIDI or audio.

```
score -> structure -> symbols -> written events -> voices/measures
      -> semantic validation -> sounding events -> MIDI
```

A discovered weakness becomes an engine improvement only when:
1. the rule is implemented in the engine;
2. a regression test reproduces the failure;
3. the regression passes;
4. the source score is reprocessed from scratch.

## Web app

1. Upload a PDF score.
2. Watch processing stages.
3. Download the MIDI result.

Current status: early engine integration. Unsupported or ambiguous notation is preserved as a diagnostic instead of silently repaired downstream.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:8000
