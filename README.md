# Integrantes: Henzo Puchetti RM555179 / Luann Mariano - RM558548 / Caio Cesar Rosa Nyimi - RM556331

# 🏍️ Detecção de Motos em Vídeo com YOLOv5

Este projeto implementa um **sistema de visão computacional** para detecção de múltiplas motos em tempo real utilizando o modelo **YOLOv5**.  

O script processa um vídeo de entrada (`Motos.mp4`), identifica motos quadro a quadro e exibe o resultado visual em uma janela interativa.  
Além disso, todas as detecções são **salvas em um arquivo CSV**, permitindo persistência dos dados e posterior análise.

---

## 🚀 Funcionalidades

✔️ Carregamento do modelo **YOLOv5 pré-treinado** (torch hub).  
✔️ **Leitura de vídeo** a partir de arquivo (`Motos.mp4`) ou webcam.  
✔️ **Detecção de motos em tempo real** com bounding boxes e rótulos de confiança.  
✔️ Exibição de saída visual em janela redimensionável no **OpenCV**.  
✔️ **Redimensionamento do vídeo** para melhor visualização (1000x600).  
✔️ **Persistência em CSV** com os seguintes dados por detecção:  
   - Timestamp (em segundos)  
   - Classe detectada (label)  
   - Confiança da detecção  
   - Coordenadas do bounding box (`x1, y1, x2, y2`)  
✔️ Encerramento manual do programa pressionando a tecla **`q`**.  

---

## 📂 Estrutura do Projeto

```
Challenge-IOT/
│── Motos.mp4                 # Vídeo de entrada
│── Motos2.mp4                 # Outra opção de video de entrada
│── Challenge-IOT.py          # Codigo principal
│── resultados_motos.csv      # Depois de rodar o projeto esse arquivo aparecerá na pasta
│── requirements.txt          # Dependências do projeto
│── README.md                 # Documentação do projeto
```

---

## ⚙️ Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`:

```txt
torch>=2.0.0
torchvision>=0.15.0
torchaudio>=2.0.0
opencv-python>=4.8.0
tqdm>=4.66.0
numpy>=1.25.0
pandas>=2.0.0
```

---

## ▶️ Como Executar

1. Clone ou baixe este repositório.  
2. Certifique-se de ter o vídeo `Motos.mp4` na mesma pasta do script.  
3. Crie um ambiente virtual (opcional, mas recomendado):  

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

4. Instale as dependências a partir do `requirements.txt`:  

```bash
pip install -r requirements.txt
```

5. Execute o script:  

```bash
python Challenge-IOT.py
```

---

## 📊 Saída

### 🎥 Janela de vídeo  
- Cada moto detectada é destacada com uma **caixa verde** e a **confiança** da predição.  
- A janela pode ser redimensionada livremente.  
- Pressione **`q`** para encerrar a execução.  

### 📑 Arquivo CSV (`resultados_motos.csv`)  
O script gera um arquivo CSV com as detecções, no formato:  

```
timestamp,label,confiança,x1,y1,x2,y2
0.25,motorcycle,0.87,123,45,300,400
0.27,motorcycle,0.91,500,60,700,350
...
```

- **timestamp** → tempo no vídeo em segundos  
- **label** → classe detectada (neste caso, sempre `motorcycle`)  
- **confiança** → score de 0 a 1 indicando a certeza da detecção  
- **x1, y1, x2, y2** → coordenadas da caixa delimitadora no frame  

---
 
