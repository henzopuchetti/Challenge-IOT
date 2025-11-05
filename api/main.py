# api/main.py
import os
import sqlite3
from typing import Optional, List, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

DB_PATH = os.getenv(
    "DB_PATH",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "detec_motos.db"))
)

app = FastAPI(title="Challenge IOT - API de Detecções (read-only)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

def get_conn(readonly: bool = True) -> sqlite3.Connection:
    uri = f"file:{DB_PATH}?mode={'ro' if readonly else 'rw'}&cache=shared"
    con = sqlite3.connect(uri, timeout=5.0, uri=True, check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA busy_timeout = 5000;")
    return con

def ensure_db_exists():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Banco não encontrado em {DB_PATH}")

@app.on_event("startup")
def startup():
    ensure_db_exists()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/videos")
def listar_videos():
    sql = """
      SELECT
        video_file,
        COUNT(*) AS total_registros,
        MIN(timestamp) AS primeiro_timestamp,
        MAX(timestamp) AS ultimo_timestamp
      FROM detections
      GROUP BY video_file
      ORDER BY video_file
    """
    with get_conn() as con:
        rows = con.execute(sql).fetchall()
    return [dict(r) for r in rows]

# ---------- Helper interno (sem Query) ----------
def _fetch_dados_do_video(
    video: str,
    limit: int,
    offset: int,
    label: Optional[str],
    from_ts: Optional[str],
    to_ts: Optional[str],
):
    base = "SELECT rowid AS id, * FROM detections WHERE video_file = ?"
    params: List[Any] = [video]

    # Use checagem explícita contra None para evitar objetos Query
    if label is not None and label != "":
        base += " AND label = ?"
        params.append(label)
    if from_ts is not None and from_ts != "":
        base += " AND timestamp >= ?"
        params.append(from_ts)
    if to_ts is not None and to_ts != "":
        base += " AND timestamp <= ?"
        params.append(to_ts)

    base += " ORDER BY COALESCE(timestamp, rowid) LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    with get_conn() as con:
        rows = con.execute(base, params).fetchall()
    return [dict(r) for r in rows]

@app.get("/videos/{video}/dados")
def dados_do_video(
    video: str,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    label: Optional[str] = None,
    from_ts: Optional[str] = Query(None, description="timestamp inicial (>=)"),
    to_ts: Optional[str] = Query(None, description="timestamp final (<=)"),
):
    return _fetch_dados_do_video(video, limit, offset, label, from_ts, to_ts)

# Alias simplificado que não passa objetos Query
@app.get("/verdados/{video}")
def verdados_alias(video: str, limit: int = 100, offset: int = 0):
    return _fetch_dados_do_video(video, limit, offset, label=None, from_ts=None, to_ts=None)

@app.get("/videos/{video}/resumo")
def resumo_do_video(video: str):
    with get_conn() as con:
        total = con.execute(
            "SELECT COUNT(*) AS total FROM detections WHERE video_file = ?", (video,)
        ).fetchone()
        if not total or total["total"] == 0:
            raise HTTPException(status_code=404, detail="Vídeo não encontrado ou sem registros")

        por_label = con.execute(
            "SELECT COALESCE(label, 'desconhecido') AS label, COUNT(*) AS qtd "
            "FROM detections WHERE video_file = ? "
            "GROUP BY COALESCE(label, 'desconhecido') ORDER BY qtd DESC",
            (video,),
        ).fetchall()

        jan_tempo = con.execute(
            "SELECT MIN(timestamp) AS primeiro_timestamp, MAX(timestamp) AS ultimo_timestamp "
            "FROM detections WHERE video_file = ?",
            (video,),
        ).fetchone()

    return {
        "video_file": video,
        "total_registros": total["total"],
        "por_label": [dict(r) for r in por_label],
        "primeiro_timestamp": jan_tempo["primeiro_timestamp"],
        "ultimo_timestamp": jan_tempo["ultimo_timestamp"],
    }
