
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

# 📊 Gráfico Personalizado com Seletores
st.subheader("🎛️ Gráfico Personalizado de Participação")

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
tipos_grafico = ["Barra", "Pizza", "Linha"]

col1, col2, col3 = st.columns(3)
with col1:
    dimensao_escolhida = st.selectbox("Agrupar por:", list(dimensoes.keys()))
with col2:
    situacao_escolhida = st.selectbox("Filtrar por:", list(situacoes.keys()))
with col3:
    tipo_grafico = st.selectbox("Tipo de Gráfico:", tipos_grafico)

coluna_agrupamento = dimensoes[dimensao_escolhida]
filtro_coluna = situacoes[situacao_escolhida]

df_plot = df if not filtro_coluna else df[df[filtro_coluna] == "Sim"]

st.markdown(f"🔍 Total de registros considerados: {len(df_plot)}")

if coluna_agrupamento in df_plot.columns:
    contagem = df_plot[coluna_agrupamento].value_counts().sort_values(ascending=False)

    if tipo_grafico == "Barra":
        st.bar_chart(contagem)
    elif tipo_grafico == "Linha":
        st.line_chart(contagem)
    elif tipo_grafico == "Pizza":
        fig, ax = plt.subplots()
        contagem.plot.pie(autopct="%1.1f%%", ax=ax)
        ax.set_ylabel("")
        ax.set_title(f"{dimensao_escolhida}")
        st.pyplot(fig)
else:
    st.warning("Coluna selecionada não encontrada.")

# Conclusões + Soluções
st.markdown("""
# 📌 Conclusões

- O prêmio tem crescido anualmente.  
- A participação feminina ainda é menor que a masculina.  
- Poesia e romance são os gêneros mais inscritos.  
- O Brasil domina em número de autores, mas há presença internacional relevante.  

---

## 💡 Soluções Propostas

### 1. 📢 Incentivo à Participação de Autores Sub-representados
- Campanhas direcionadas a países lusófonos com baixa participação (ex: Moçambique, Angola, Timor-Leste).
- Parcerias com editoras locais e coletivos literários nesses países.
- Criação de categorias especiais ou cotas de destaque para autores desses territórios.

### 2. 🚻 Ações de Equidade de Gênero
- Estímulo à inscrição de mulheres, pessoas trans e não-binárias com ações afirmativas ou premiações paralelas.
- Inclusão de indicadores de gênero e diversidade nos relatórios públicos do prêmio.
- Painel de acompanhamento anual para verificar a evolução da representatividade.

### 3. 📚 Diversificação de Gêneros Literários
- Criação de chamadas temáticas para incentivar gêneros pouco inscritos, como crônica, ensaio e dramaturgia.
- Workshops ou mentorias para novos autores nesses gêneros.
- Premiação de categorias por gênero literário.

### 4. 📊 Painel BI Público com Indicadores de Diversidade
- Desenvolver um painel (como este app Streamlit) com:
  - Evolução de inscrições por gênero, país e faixa etária.
  - Comparativos entre inscritos, finalistas e vencedores.
  - Filtros interativos para consulta por ano, país ou gênero literário.

🎯 Objetivo: garantir **transparência**, promover **equidade** e permitir que a curadoria do prêmio se apoie em **dados reais** para decisões mais inclusivas.
""")
