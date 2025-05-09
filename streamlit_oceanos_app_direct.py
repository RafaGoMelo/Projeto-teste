
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

# 📈 Exemplo de gráfico: Vencedores
st.subheader("🏆 Distribuição de Vencedores")
fig1, ax1 = plt.subplots()
df.groupby('Vencedor').size().plot(kind='barh', color=sns.color_palette('Dark2'), ax=ax1)
ax1.set_title("Distribuição de Vencedores")
ax1.spines[['top', 'right']].set_visible(False)
st.pyplot(fig1)

# 📊 Exemplo de gráfico: Gênero do Autor
st.subheader("👤 Distribuição por Gênero dos Autores")
fig2, ax2 = plt.subplots()
df.groupby('GeneroAutor').size().plot(kind='barh', color=sns.color_palette('Dark2'), ax=ax2)
ax2.set_title("Gênero dos Autores")
ax2.spines[['top', 'right']].set_visible(False)
st.pyplot(fig2)

# 📚 Exemplo de gráfico: Gênero Literário
st.subheader("📚 Distribuição por Gênero Literário")
fig3, ax3 = plt.subplots()
df['GeneroLivro'].value_counts().plot(kind='bar', color=sns.color_palette('Dark2'), ax=ax3)
ax3.set_title("Gêneros Literários")
ax3.set_ylabel("Quantidade")
ax3.set_xlabel("Gênero")
ax3.spines[['top', 'right']].set_visible(False)
st.pyplot(fig3)

# 🔍 Análise Avançada: Gênero mais presente entre finalistas
st.subheader("📖 Gêneros Literários entre Finalistas")
finalistas = df[df['Finalista'] == 'Sim']
fig4, ax4 = plt.subplots()
sns.countplot(y='GeneroLivro', data=finalistas, order=finalistas['GeneroLivro'].value_counts().index, ax=ax4)
ax4.set_title("Finalistas por Gênero Literário")
st.pyplot(fig4)

# Funções de Análise OLAP
def contar_finalistas_por_genero(df):
    st.subheader("📌 Finalistas por Gênero do Autor")
    contagem = df[df['Finalista'] == 'Sim']['GeneroAutor'].value_counts()
    st.bar_chart(contagem)

def generos_mais_premiados(df):
    st.subheader("🏅 Gêneros Literários mais Premiados")
    contagem = df[df['Vencedor'] == 'Sim']['GeneroLivro'].value_counts()
    st.bar_chart(contagem)

def finalistas_por_pais(df, top_n=10):
    st.subheader("🌍 Finalistas por País")
    contagem = df[df['Finalista'] == 'Sim']['PaisAutor'].value_counts().head(top_n)
    st.bar_chart(contagem)

def autoras_mulheres_por_ano(df):
    st.subheader("📈 Evolução de Autoras Mulheres por Ano")
    mulheres = df[df['GeneroAutor'] == 'Feminino'].groupby('Ano').size()
    st.line_chart(mulheres)

def cruzamento_finalistas(df, genero=None, pais=None):
    st.subheader("🎯 Consulta por Gênero e País entre Finalistas")
    filtro = df[df['Finalista'] == 'Sim']
    if genero:
        filtro = filtro[filtro['GeneroAutor'] == genero]
    if pais:
        filtro = filtro[filtro['PaisAutor'] == pais]
    st.write(f"Total encontrado: {filtro.shape[0]}")
    st.dataframe(filtro[['Ano', 'TituloLivro', 'GeneroLivro', 'NomeAutor', 'GeneroAutor', 'PaisAutor']])

# ⬛ Executando funções interativas
contar_finalistas_por_genero(df)
generos_mais_premiados(df)
finalistas_por_pais(df)
autoras_mulheres_por_ano(df)
cruzamento_finalistas(df, genero="Feminino", pais="Portugal")

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
