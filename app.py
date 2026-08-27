"""Portfólio pessoal de João Gilbert Agrelle."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, render_template, send_from_directory


BASE_DIR = Path(__file__).resolve().parent
ORIGINAL_CURRICULUM_FILENAME = "Curriculo_Joao_Gilbert_Agrelle.pdf"
UPDATED_CURRICULUM_FILENAME = "Curriculo_Joao_Gilbert_Agrelle_Atualizado.pdf"

app = Flask(__name__)


@app.get("/")
def index():
    """Renderiza a página principal do portfólio."""
    return render_template("index.html")


@app.get("/api/status")
def profile_status():
    """Expõe os dados dinâmicos usados pelo terminal da interface."""
    return jsonify(
        {
            "name": "João Gilbert Agrelle",
            "role": "Desenvolvedor Java em formação",
            "location": "Recife, PE",
            "availability": "Buscando estágio em Backend e IA Generativa",
            "status": "online",
        }
    )


@app.get("/curriculo")
def download_curriculum():
    """Disponibiliza o currículo original para download."""
    return send_from_directory(
        BASE_DIR / "output" / "pdf",
        UPDATED_CURRICULUM_FILENAME,
        as_attachment=True,
        download_name=UPDATED_CURRICULUM_FILENAME,
    )


@app.get("/curriculo/original")
def download_original_curriculum():
    return send_from_directory(
        BASE_DIR,
        ORIGINAL_CURRICULUM_FILENAME,
        as_attachment=True,
        download_name=ORIGINAL_CURRICULUM_FILENAME,
    )




@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
