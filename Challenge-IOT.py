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
