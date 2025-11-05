# 🏍️ Detecção de Motos em Vídeo com YOLOv5

Este projeto implementa um **sistema de visão computacional** para detecção de motos em vídeos utilizando o modelo **YOLOv5**.  

O sistema processa o vídeo de entrada (`Motos.mp4`), identifica motos quadro a quadro, desenha bounding boxes no frame e **gera logs enriquecidos** em CSV e em **banco de dados SQLite**.  

Além disso, o projeto conta com um **dashboard em Streamlit** para visualização e análise dos dados detectados.  

---

# Integrantes  
Henzo Puchetti – RM555179  
Luann Mariano – RM558548  
Caio Cesar Rosa Nyimi – RM556331  

---

## 🚀 Funcionalidades

✔️ Carregamento do modelo **YOLOv5 pré-treinado** (Torch Hub).  
✔️ **Leitura de vídeo** a partir de arquivo (`Motos.mp4`) ou webcam.  
✔️ **Detecção de motos em tempo real** com bounding boxes e rótulos de confiança.  
✔️ Exibição da saída visual em janela redimensionável no **OpenCV**.  
✔️ **Logs enriquecidos**:
- `frame_id` (identificação do frame)  
- `timestamp` (tempo em segundos no vídeo)  
- `video_file` (nome do arquivo analisado)  
- `total_motos` (contador acumulado de motos)  
- `label` (classe detectada – sempre `motorcycle`)  
- `confiança` da predição  
- coordenadas do bounding box (`x1, y1, x2, y2`)  

✔️ **Persistência dupla**:  
- CSV (`resultados_motos.csv`)  
- Banco de dados **SQLite** (`detec_motos.db`)  

✔️ **Dashboard interativo (Streamlit)** com tabelas e gráficos.  

**🆕 API HTTP (FastAPI)** para **acessar os dados do SQLite por URL** (GET).  
- Endpoints principais:
  - `GET /health` – status da API  
  - `GET /videos` – lista os vídeos presentes no banco com totais  
  - `GET /verdados/{video}` – **retorna os registros daquele vídeo** (atalho)  
  - `GET /videos/{video}/dados?limit=&offset=&label=&from_ts=&to_ts=` – dados do vídeo com filtros e paginação  
  - `GET /videos/{video}/resumo` – resumo (totais e janelas de tempo)

> Observação: o writer habilita **WAL** no SQLite para permitir leitura pela API enquanto o vídeo ainda está sendo processado.

---

## 📂 Estrutura do Projeto

```
Challenge-IOT/
│── Motos.mp4                 # Vídeo de entrada
│── Motos2.mp4                # (opcional) segundo vídeo
│── Challenge-IOT.py          # Código principal (detecção e logs → CSV/SQLite)
│── resultados_motos.csv      # Arquivo CSV gerado com as detecções
│── detec_motos.db            # Banco SQLite com os dados
│── dashboard.py              # Dashboard em Streamlit (análise)
│── requirements.txt          # Dependências do projeto
│── README.md                 # Documentação do projeto
└── api/
    └── main.py               # 🆕 API FastAPI que expõe o SQLite por URL
```

---

## ⚙️ Dependências

As dependências estão listadas no arquivo `requirements.txt`. Principais grupos:

```txt
# Deep Learning / Visão Computacional
torch>=2.0.0
torchvision>=0.15.0
torchaudio>=2.0.0
opencv-python>=4.8.0
ultralytics>=8.0.0

# Utilidades
tqdm>=4.66.0
numpy>=1.25.0
pandas>=2.0.0

# Banco de Dados
sqlite-utils>=3.36.0

# Dashboard e Visualização
streamlit>=1.27.0
matplotlib>=3.7.0
seaborn>=0.12.2

# 🆕 API HTTP
fastapi>=0.115.0
uvicorn>=0.32.0
# (opcional para produção)
gunicorn>=21.2.0
```

---

## ▶️ Como Executar

### 1) Preparar ambiente
```bash
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

### 2) Rodar o detector de motos (gera CSV e SQLite)
```bash
python Challenge-IOT.py
```
- A janela do OpenCV será aberta; pressione **`q`** para encerrar.  
- O banco `detec_motos.db` e o arquivo `resultados_motos.csv` serão criados/atualizados.

### 3) 🆕 Subir a API (para acessar o banco via URL)
Em um **segundo terminal** (com a venv ativa):
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
Acesse a documentação (Swagger):  
`http://localhost:8000/docs`

**Exemplos de GET**:
- `http://localhost:8000/health`  
- `http://localhost:8000/videos`  
- `http://localhost:8000/verdados/Motos2.mp4`  
- `http://localhost:8000/videos/Motos2.mp4/dados?limit=50&offset=0`  
- `http://localhost:8000/videos/Motos2.mp4/dados?label=motorcycle&limit=100`  
- `http://localhost:8000/videos/Motos2.mp4/resumo`

> Dica: se o banco estiver em outro caminho/nome, defina `DB_PATH` antes de subir a API.  
> Ex.: `set DB_PATH=C:\caminho\detec_motos.db` (Windows) / `export DB_PATH=/caminho/detec_motos.db` (Linux/Mac)

### 4) (Opcional) Abrir o dashboard (análise)
```bash
streamlit run dashboard.py
```
Acesse: [http://localhost:8501](http://localhost:8501)

---

## 📊 Saída

### 🎥 Vídeo em tempo real
- Cada moto detectada é destacada com uma **caixa verde** e a **confiança da detecção**.  
- A janela é redimensionável.  
- Pressione **`q`** para encerrar a execução.  

### 📑 Arquivo CSV (`resultados_motos.csv`)
Contém as detecções em formato tabular:
```
frame_id,timestamp,video_file,total_motos,label,confiança,x1,y1,x2,y2
15,0.25,Motos.mp4,1,motorcycle,0.87,123,45,300,400
16,0.27,Motos.mp4,2,motorcycle,0.91,500,60,700,350
...
```

### 🗄️ Banco de Dados (`detec_motos.db`)
- Todos os dados também são persistidos no SQLite.  
- Exemplos rápidos de consulta:
  ```sql
  SELECT COUNT(*) FROM detections WHERE label='motorcycle';
  SELECT * FROM detections WHERE video_file='Motos2.mp4' LIMIT 10;
  ```

### 📈 Dashboard (Streamlit)
- Tabela interativa com os registros.  
- Gráfico da evolução das detecções ao longo do tempo.  
- Gráfico de total acumulado de motos.  

---

## ℹ️ Notas Técnicas (API + Banco)
- O `Challenge-IOT.py` habilita **`PRAGMA journal_mode=WAL`**, **`busy_timeout`** e **`synchronous=NORMAL`** para melhorar a convivência entre **escrita contínua** (durante o vídeo) e **leituras** pela API.  
- A API utiliza conexão **read-only** por padrão e paginação nos endpoints.  
- CORS liberado para **GET** (ajuste `allow_origins` no `api/main.py` se precisar restringir).
