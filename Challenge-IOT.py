import torch
import cv2
import csv
import sqlite3

#Config
VIDEO_FILE = "Motos2.mp4"
DB_FILE = "detec_motos.db"
CSV_FILE = "resultados_motos.csv"

#Banco de dados
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    frame_id INTEGER,
    timestamp REAL,
    video_file TEXT,
    total_motos INTEGER,
    label TEXT,
    confianca REAL,
    x1 INTEGER,
    y1 INTEGER,
    x2 INTEGER,
    y2 INTEGER
)
""")
conn.commit()

#arquivo csv
csv_file = open(CSV_FILE, mode="w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow([
    "frame_id", "timestamp", "video_file",
    "total_motos", "label", "confiança", "x1", "y1", "x2", "y2"
])

#yolo
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
cap = cv2.VideoCapture(VIDEO_FILE)

if not cap.isOpened():
    print("Erro ao abrir o vídeo")
    exit()

cv2.namedWindow('YOLOv5 - Detecção de Motos', cv2.WINDOW_NORMAL)

frame_id = 0
total_motos = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1
    frame = cv2.resize(frame, (1000, 600))
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = model(img_rgb, size=640)
    timestamp = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, 2)

    for *box, conf, cls in results.xyxy[0]:
        label = results.names[int(cls)]
        if label == "motorcycle":
            x1, y1, x2, y2 = map(int, box)
            total_motos += 1

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'MOTO {conf:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            csv_writer.writerow([
                frame_id, timestamp, VIDEO_FILE,
                total_motos, label, float(conf), x1, y1, x2, y2
            ])

            cursor.execute("""
                INSERT INTO detections (
                    frame_id, timestamp, video_file,
                    total_motos, label, confianca, x1, y1, x2, y2
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                frame_id, timestamp, VIDEO_FILE,
                total_motos, label, float(conf), x1, y1, x2, y2
            ))
            conn.commit()

    cv2.imshow('YOLOv5 - Detecção de Motos', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
csv_file.close()
conn.close()
cv2.destroyAllWindows()
import os
import torch
import cv2
import csv
import sqlite3

# =========================
# Config
# =========================
VIDEO_FILE = os.getenv("VIDEO_FILE", "Motos2.mp4")
DB_FILE = os.getenv("DB_FILE", "detec_motos.db")
CSV_FILE = os.getenv("CSV_FILE", "resultados_motos.csv")

# =========================
# Banco de dados (writer)
# =========================
conn = sqlite3.connect(DB_FILE, timeout=5.0, check_same_thread=False)
cursor = conn.cursor()

# Modo WAL para coexistir com a API (leituras sem bloquear a escrita)
cursor.execute("PRAGMA journal_mode = WAL;")
# Menos fsync (bom para vídeo em tempo real)
cursor.execute("PRAGMA synchronous = NORMAL;")
# Tempo de espera amigável antes de dar lock error
cursor.execute("PRAGMA busy_timeout = 5000;")
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    frame_id INTEGER,
    timestamp REAL,
    video_file TEXT,
    total_motos INTEGER,
    label TEXT,
    confianca REAL,
    x1 INTEGER,
    y1 INTEGER,
    x2 INTEGER,
    y2 INTEGER
)
""")
# Índices para acelerar os GETs da API
cursor.execute("CREATE INDEX IF NOT EXISTS idx_detections_video ON detections(video_file);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_detections_video_ts ON detections(video_file, timestamp);")
conn.commit()

# =========================
# Arquivo CSV
# =========================
csv_file = open(CSV_FILE, mode="w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow([
    "frame_id", "timestamp", "video_file",
    "total_motos", "label", "confiança", "x1", "y1", "x2", "y2"
])

# =========================
# YOLOv5 (torch.hub)
# =========================
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
cap = cv2.VideoCapture(VIDEO_FILE)

if not cap.isOpened():
    print(f"Erro ao abrir o vídeo: {VIDEO_FILE}")
    csv_file.close()
    conn.close()
    raise SystemExit(1)

cv2.namedWindow('YOLOv5 - Detecção de Motos', cv2.WINDOW_NORMAL)

frame_id = 0
total_motos = 0  # contador cumulativo (mantido como estava)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_id += 1
        frame = cv2.resize(frame, (1000, 600))
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = model(img_rgb, size=640)
        timestamp = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, 2)

        # Inserções ficam em uma única transação por frame
        inserts = []

        for *box, conf, cls in results.xyxy[0]:
            label = results.names[int(cls)]
            if label == "motorcycle":
                x1, y1, x2, y2 = map(int, box)
                total_motos += 1

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'MOTO {float(conf):.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                csv_writer.writerow([
                    frame_id, timestamp, VIDEO_FILE,
                    total_motos, label, float(conf), x1, y1, x2, y2
                ])

                inserts.append((
                    frame_id, timestamp, VIDEO_FILE,
                    total_motos, label, float(conf), x1, y1, x2, y2
                ))

        if inserts:
            cursor.executemany("""
                INSERT INTO detections (
                    frame_id, timestamp, video_file,
                    total_motos, label, confianca, x1, y1, x2, y2
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, inserts)
            conn.commit()

        cv2.imshow('YOLOv5 - Detecção de Motos', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    csv_file.close()
    conn.close()
    cv2.destroyAllWindows()
