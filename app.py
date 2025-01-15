import streamlit as st
import pandas as pd
import random
import os

# Configurar o modo wide
st.set_page_config(layout="wide", page_title="Avaliação LLM", page_icon='🤖')


# Nome do arquivo CSV onde os dados serão armazenados
CSV_FILE_ANSWERS = "data/respostas_usuarios.csv"
CSV_FILE_ORIGIN = "data/fr1.csv"
FR_TEXT = "data/fr1.txt"

# Verifica se o arquivo existe, se não, cria com colunas padrão
if not os.path.exists(CSV_FILE_ANSWERS):
    pd.DataFrame(columns=["Texto 1", "Texto 2", "Resposta 1", "Resposta 2", "Resposta 3", "Comentários"]).to_csv(CSV_FILE_ANSWERS, index=True)

# Verifica se o arquivo existe, se não, cria o texto padrão
if not os.path.exists(FR_TEXT):
    df = pd.read_csv(CSV_FILE_ORIGIN)
    with open(FR_TEXT, "w") as f:
        f.write("{}".format(df['fr'][0]))

# Função para carregar os textos a partir de um CSV
@st.cache_data
def load_texts():
    return pd.read_csv("data/fr1.csv")


# Função para selecionar dois textos aleatórios
def select_random_texts(df):
    pair = random.sample(df.index.tolist(), 2)
    return df.loc[pair[0]], df.loc[pair[1]]

# Título
st.title("Avaliação LLM 🤖")

# Instruções
st.markdown("""
### Bem-vindo!
TEXTO INTRODUTÓRIO
            
Abaixo você encontrará dois textos gerados por um modelo de linguagem.
            
Vale a pena deixar acesso ao Documento que foi feita a análise?
""")

st.download_button('Download Documento Original', FR_TEXT)


# Carrega os textos
textos_df = load_texts()

# Seleciona dois textos aleatórios
texto1, texto2 = select_random_texts(textos_df)

# Apresenta os textos
st.markdown("### Textos Selecionados")
col1, col2 = st.columns(2)

with col1:
    st.header("Análise 1")
    st.markdown(texto1["generated_text"])

with col2:
    st.header("Análise 2")
    st.markdown(texto2["generated_text"])

# Formulário para avaliação
st.markdown("### Avaliação")
with st.form("avaliacao_form"):
    st.write("Responda as perguntas abaixo:")
    
    resposta1 = st.radio("Qual texto é mais claro?", ["Texto 1", "Texto 2", "Ambos"])
    resposta2 = st.radio("Qual texto é mais informativo?", ["Texto 1", "Texto 2", "Ambos"])
    resposta3 = st.slider("Dê uma nota geral para os textos (1 a 10):", 1, 10)
    comentarios = st.text_area("Comentários ou sugestões (opcional):")
    enviado = st.form_submit_button("Enviar")

    if enviado:
        
        # Adicionar os novos dados
        novo_dado = {
            "Texto 1": texto1["generated_text"],
            "Texto 2": texto2["generated_text"],
            "Resposta 1": resposta1,
            "Resposta 2": resposta2,
            "Resposta 3": resposta3,
            "Comentários": comentarios,
        }

        novo_df = pd.DataFrame(novo_dado, index=[0])

        try:
            novo_df.to_csv(CSV_FILE_ANSWERS, mode="a", header=False, index=False)
            st.success("Respostas enviadas com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar os dados: {e}")
        
        st.success("Respostas enviadas com sucesso!")
