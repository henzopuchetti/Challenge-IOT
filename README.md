# Integrantes  
Henzo Puchetti – RM555179  
Luann Mariano – RM558548  
Caio Cesar Rosa Nyimi – RM556331  

# 🏍️ Detecção de Motos em Vídeo com YOLOv5

Este projeto implementa um **sistema de visão computacional** para detecção de motos em vídeos utilizando o modelo **YOLOv5**.  

O sistema processa o vídeo de entrada (`Motos.mp4`), identifica motos quadro a quadro, desenha bounding boxes no frame e **gera logs enriquecidos** em CSV e em **banco de dados SQLite**.  

Além disso, o projeto conta com um **dashboard em Streamlit** para visualização e análise dos dados detectados.  

---

## 🚀 Funcionalidades

✔️ Carregamento do modelo **YOLOv5 pré-treinado** (Torch Hub).  
✔️ **Leitura de vídeo** a partir de arquivo (`Motos.mp4`, `Motos2.mp4`) ou webcam.  
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
✔️ **Dashboard interativo (Streamlit)** com tabelas e gráficos:  
   - Evolução do número de motos ao longo do tempo  
   - Total acumulado de detecções  
   - Estatísticas básicas para análise  
✔️ Encerramento manual do programa pressionando a tecla **`q`**.  

---

## 📂 Estrutura do Projeto

```
Challenge-IOT/
│── Motos.mp4                 # Vídeo de entrada
│── Motos2.mp4                # Outra opção de vídeo de entrada
│── Challenge-IOT.py          # Código principal (detecção e logs)
│── resultados_motos.csv      # Arquivo CSV gerado com as detecções
│── detec_motos.db            # Banco SQLite com os dados (após execução)
│── dashboard.py              # Dashboard em Streamlit para análise
│── requirements.txt          # Dependências do projeto
│── README.md                 # Documentação do projeto
```

---

## ⚙️ Dependências

As dependências estão listadas no arquivo `requirements.txt`:  

```txt
# Deep Learning / Visão Computacional
torch>=2.0.0
torchvision>=0.15.0
torchaudio>=2.0.0
opencv-python>=4.8.0

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

# Comunicação (IoT futuro - opcional)
paho-mqtt>=1.6.1
```

---

## ▶️ Como Executar

### 1. Preparar ambiente
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 2. Rodar o detector de motos
```bash
python Challenge-IOT.py
```

### 3. Abrir o dashboard (análise)
```bash
streamlit run dashboard.py
```
Acesse no navegador: [http://localhost:8501](http://localhost:8501)

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
- Pode ser consultado via **SQLite CLI**, **DB Browser for SQLite** ou com Pandas.  
- Exemplo de consulta:
  ```sql
  SELECT COUNT(*) FROM detections WHERE label='motorcycle';
  ```

### 📈 Dashboard (Streamlit)
- Tabela interativa com os registros.  
- Gráfico da evolução das detecções ao longo do tempo.  
- Gráfico de total acumulado de motos.  

---
