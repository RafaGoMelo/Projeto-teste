import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Painel BI - Prêmio Oceanos de Literatura")

df = pd.read_csv("oceanos_dados_limpos_para_powerbi.csv")

tab1, tab2, tab3, tab4 = st.tabs(["📌 Visão Geral", "📈 Evolução Temporal", "🌍 Indicadores de Diversidade", "🎛️ Gráfico Personalizado"])

with tab1:
    st.header("📌 Indicadores Gerais")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Obras", len(df))
    col2.metric("Total de Autores", df['NomeAutor'].nunique())
    col3.metric("Total de Países", df['PaisAutor'].nunique())
    st.subheader("🎯 Participação por Gênero")
    st.bar_chart(df['GeneroAutor'].value_counts())
    st.subheader("📚 Gêneros Literários Mais Frequentes")
    st.bar_chart(df['GeneroLivro'].value_counts())

    st.subheader("📋 Visualização da Tabela Completa")
    st.dataframe(df, use_container_width=True)


with tab2:
    st.header("📈 Evolução ao Longo do Tempo")
    st.subheader("📅 Total de Inscrições por Ano")
    st.line_chart(df.groupby('Ano').size())
    st.subheader("🚻 Participação Feminina por Ano")
    mulheres = df[df['GeneroAutor'] == 'Feminino'].groupby('Ano').size()
    st.line_chart(mulheres)
    st.subheader("🏅 Finalistas por Ano")
    finalistas = df[df['Finalista'] == 'Sim'].groupby('Ano').size()
    st.line_chart(finalistas)

with tab3:
    st.header("🌍 Indicadores de Diversidade")
    st.subheader("🌐 Participação por País")
    st.bar_chart(df['PaisAutor'].value_counts())
    st.subheader("📊 Faixa Etária dos Autores")
    st.bar_chart(df['FaixaEtariaAutor'].value_counts())
    st.subheader("🎖️ Proporção de Vencedores por Gênero")
    vencedores = df[df['Vencedor'] == "Sim"]
    st.bar_chart(vencedores['GeneroAutor'].value_counts())

with tab4:
    st.header("🎛️ Gráfico Dinâmico por Filtro")

    # Filtros extras
    anos = st.multiselect("Ano", sorted(df["Ano"].unique()), default=sorted(df["Ano"].unique()))
    paises = st.multiselect("País do Autor", sorted(df["PaisAutor"].unique()), default=sorted(df["PaisAutor"].unique()))
    generos_autor = st.multiselect("Gênero do Autor", df["GeneroAutor"].dropna().unique(), default=df["GeneroAutor"].dropna().unique())

    # Filtros dinâmicos
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
        situacao_escolhida = st.selectbox("Filtrar por status:", list(situacoes.keys()))
    with col3:
        tipo_grafico = st.selectbox("Tipo de Gráfico:", tipos_grafico)

    # Aplicar os filtros
    df_filtrado = df[
        (df['Ano'].isin(anos)) &
        (df['PaisAutor'].isin(paises)) &
        (df['GeneroAutor'].isin(generos_autor))
    ]
    if situacoes[situacao_escolhida]:
        df_filtrado = df_filtrado[df_filtrado[situacoes[situacao_escolhida]] == "Sim"]

    coluna_agrupamento = dimensoes[dimensao_escolhida]

    st.markdown(f"🔍 Total de registros após filtros: {len(df_filtrado)}")

    if coluna_agrupamento in df_filtrado.columns:
        contagem = df_filtrado[coluna_agrupamento].value_counts().sort_values(ascending=False)

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

