from pathlib import Path
from uuid import uuid4
from flask import Flask, jsonify, render_template, request, send_file
from engine import ChoirOMREngine

app = Flask(__name__)
JOBS = Path("jobs")
JOBS.mkdir(exist_ok=True)
engine = ChoirOMREngine()
status = {}

@app.get("/")
def index():
    return render_template("index.html", engine_version=engine.VERSION)

@app.post("/process")
def process():
    upload = request.files.get("score")
    if not upload or not upload.filename:
        return jsonify(error="Choose a PDF score."), 400
    if not upload.filename.lower().endswith(".pdf"):
        return jsonify(error="Current build accepts PDF scores only."), 400

    job_id = uuid4().hex
    folder = JOBS / job_id
    folder.mkdir()
    source = folder / "score.pdf"
    midi = folder / "result.mid"
    upload.save(source)
    status[job_id] = {"stage": "Queued", "percent": 0}

    def progress(stage, percent):
        status[job_id] = {"stage": stage, "percent": percent}

    result = engine.process(source, midi, progress)
    status[job_id].update({
        "passed": result.passed,
        "diagnostics": result.diagnostics,
        "download": f"/download/{job_id}" if result.passed else None,
    })
    return jsonify(job_id=job_id, **status[job_id])

@app.get("/status/<job_id>")
def job_status(job_id):
    return jsonify(status.get(job_id, {"stage": "Unknown job", "percent": 0}))

@app.get("/download/<job_id>")
def download(job_id):
    midi = JOBS / job_id / "result.mid"
    if not midi.exists():
        return jsonify(error="No validated MIDI exists for this job."), 404
    return send_file(midi, as_attachment=True, download_name="choir-omr.mid")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
