import torch
import cv2
import csv
import time

# Carrega o modelo YOLOv5 pré-treinado
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Abre o vídeo (ou use 0 para webcam)
cap = cv2.VideoCapture('Motos.mp4')

if not cap.isOpened():
    print("Erro ao abrir o vídeo")
    exit()

# Cria arquivo CSV para salvar resultados
csv_file = open("resultados_motos.csv", mode="w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["timestamp", "label", "confiança", "x1", "y1", "x2", "y2"])

# Define a janela como redimensionável
cv2.namedWindow('YOLOv5 - Detecção de Motos', cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Redimensiona o frame para caber na janela
    frame = cv2.resize(frame, (1000, 600))

    # Converte de BGR para RGB
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Faz a detecção
    results = model(img_rgb, size=640)

    # Marca o timestamp (em segundos)
    timestamp = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, 2)

    # Percorre os objetos detectados
    for *box, conf, cls in results.xyxy[0]:
        label = results.names[int(cls)]
        if label == 'motorcycle':
            x1, y1, x2, y2 = map(int, box)

            # Desenha retângulo no vídeo
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label.upper()} {conf:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Salva no CSV
            csv_writer.writerow([timestamp, label, float(conf), x1, y1, x2, y2])

    # Mostra o frame redimensionado
    cv2.imshow('YOLOv5 - Detecção de Motos', frame)

    # Espera 1 milissegundo (pressione 'q' para sair)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
csv_file.close()
cv2.destroyAllWindows()
