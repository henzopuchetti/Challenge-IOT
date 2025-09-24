import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_FILE = "detec_motos.db"

#conexao e leitura de dados
conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query("SELECT * FROM detections", conn)
conn.close()

st.title("📊 Dashboard de Detecção de Motos")

st.write("### Dados brutos")
st.dataframe(df.head(20))

#grafico de evolução
st.write("### Evolução das detecções ao longo do tempo")
fig, ax = plt.subplots()
df.groupby("timestamp").size().plot(ax=ax)
ax.set_xlabel("Tempo (s)")
ax.set_ylabel("Qtde de Motos")
st.pyplot(fig)

#grafico acumulado
st.write("### Total acumulado de motos")
fig2, ax2 = plt.subplots()
df["total_motos"].plot(ax=ax2)
ax2.set_xlabel("Frame")
ax2.set_ylabel("Total acumulado")
st.pyplot(fig2)
