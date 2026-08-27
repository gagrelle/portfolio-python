"""Portfólio pessoal de João Gilbert Agrelle."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, render_template, send_from_directory


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

@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
