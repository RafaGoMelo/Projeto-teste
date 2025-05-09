
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📘 Análise Interativa do Prêmio Oceanos de Literatura")

# 📄 Introdução
st.markdown("""
Este projeto analisa os dados históricos do Prêmio Oceanos para entender padrões de participação, diversidade de autores e gêneros, e sugerir melhorias baseadas em dados.
""")

# 📂 Leitura dos Dados
df = pd.read_csv("oceanos_dados_limpos_para_powerbi.csv")
st.subheader("📊 Pré-visualização dos dados")
st.dataframe(df, use_container_width=True)

# 📊 Gráfico personalizado OLAP com seletores
st.subheader("🎛️ Gráfico Personalizado de Participação")

# Opções de dimensões e situações
dimensoes = {
    "Gênero do Autor": "GeneroAutor",
    "Gênero Literário": "GeneroLivro",
    "País do Autor": "PaisAutor",
    "Faixa Etária do Autor": "FaixaEtariaAutor",
    "Ano": "Ano"
}
situacoes = {
    "Todos os inscritos": None,
    "Apenas Vencedores": "Vencedor",
    "Apenas Finalistas": "Finalista",
    "Apenas Semifinalistas": "Semifinalista"
}

col1, col2 = st.columns(2)
with col1:
    dimensao_escolhida = st.selectbox("Selecione o agrupamento (dimensão):", list(dimensoes.keys()))
with col2:
    situacao_escolhida = st.selectbox("Filtrar por:", list(situacoes.keys()))

coluna_agrupamento = dimensoes[dimensao_escolhida]
filtro_coluna = situacoes[situacao_escolhida]

# Aplicar filtro e gerar gráfico
if filtro_coluna:
    df_plot = df[df[filtro_coluna] == "Sim"]
else:
    df_plot = df.copy()

if coluna_agrupamento in df_plot.columns:
    grafico = df_plot[coluna_agrupamento].value_counts().sort_values(ascending=False)
    st.bar_chart(grafico)
    st.markdown(f"🔍 Total de registros considerados: {len(df_plot)}")
else:
    st.warning("Coluna selecionada não encontrada.")

# ✅ Conclusão
st.subheader("📌 Conclusões")
st.markdown("""
- O prêmio tem crescido anualmente.  
- A participação feminina ainda é menor que a masculina.  
- Poesia e romance são os gêneros mais inscritos.  
- O Brasil domina em número de autores, mas há presença internacional relevante.  

**Soluções sugeridas:**  
Incentivo a autores de países e gêneros sub-representados; criação de painel BI público com indicadores de diversidade.
""")
