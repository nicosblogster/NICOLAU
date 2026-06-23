from __future__ import annotations

import json
import re
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

from .models import ProposalSubmission, UploadedDocument


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SUBMISSIONS_DIR = DATA_DIR / "submissions"
UPLOADS_DIR = DATA_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"


def ensure_directories() -> None:
    for directory in (SUBMISSIONS_DIR, UPLOADS_DIR, OUTPUT_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def generate_protocol(full_name: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "-", full_name.strip()).strip("-").upper()
    prefix = normalized[:18] if normalized else "PROPONENTE"
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"LOC-{timestamp}-{prefix}"


def save_uploaded_file(protocol: str, label: str, uploaded_file) -> UploadedDocument | None:
    if uploaded_file is None:
        return None

    target_dir = UPLOADS_DIR / protocol
    target_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", uploaded_file.name)
    target_path = target_dir / safe_name

    uploaded_file.seek(0)
    with target_path.open("wb") as file:
        shutil.copyfileobj(uploaded_file, file)

    return UploadedDocument(
        label=label,
        filename=uploaded_file.name,
        saved_path=str(target_path),
        size_bytes=target_path.stat().st_size,
    )


def save_submission(submission: ProposalSubmission) -> Path:
    ensure_directories()
    path = SUBMISSIONS_DIR / f"{submission.protocol}.json"
    path.write_text(json.dumps(submission.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def create_submission_package(submission: ProposalSubmission, json_path: Path) -> Path:
    if not submission.pdf_path:
        raise ValueError("A proposta precisa ter um PDF antes da criacao do pacote.")

    package_path = OUTPUT_DIR / f"{submission.protocol}-documentos.zip"
    with zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(submission.pdf_path, arcname=f"{submission.protocol}.pdf")
        archive.write(json_path, arcname=f"{submission.protocol}.json")
        for document in submission.documents:
            source = Path(document.saved_path)
            if source.exists():
                archive.write(source, arcname=f"documentos/{document.label}/{source.name}")
    return package_path
