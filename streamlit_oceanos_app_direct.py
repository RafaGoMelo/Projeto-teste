
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Análise Interativa do Prêmio Oceanos de Literatura")

# Carregar o CSV diretamente do repositório
df = pd.read_csv("oceanos_dados_limpos_para_powerbi.csv")

# Filtros na barra lateral
st.sidebar.header("Filtros")
anos = st.sidebar.multiselect("Ano", sorted(df["Ano"].unique()), default=sorted(df["Ano"].unique()))
genero = st.sidebar.multiselect("Gênero do Autor", df["GeneroAutor"].unique(), default=df["GeneroAutor"].unique())
pais = st.sidebar.multiselect("País do Autor", df["PaisAutor"].unique(), default=df["PaisAutor"].unique())

df_filtrado = df[
    (df["Ano"].isin(anos)) &
    (df["GeneroAutor"].isin(genero)) &
    (df["PaisAutor"].isin(pais))
]

st.subheader("📊 Finalistas por Gênero")
finalistas = df_filtrado[df_filtrado["Finalista"] == "Sim"]
grafico_genero = finalistas["GeneroAutor"].value_counts()
st.bar_chart(grafico_genero)

st.subheader("📈 Evolução de Autoras Mulheres")
mulheres = df_filtrado[df_filtrado["GeneroAutor"] == "Feminino"].groupby("Ano").size()
st.line_chart(mulheres)

st.subheader("📚 Tabela de Finalistas")
st.dataframe(finalistas[["Ano", "TituloLivro", "NomeAutor", "GeneroLivro", "GeneroAutor", "PaisAutor"]])
