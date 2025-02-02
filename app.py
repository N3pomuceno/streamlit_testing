import streamlit as st
import pandas as pd
import random
# import io
# import os
import util

HOST = st.secrets["HOST"]
PORT = st.secrets["PORT"]
APP_SECRET_GMAIL = st.secrets["APP_SECRET_UFF_MAIL"]
APP_SECRET_GMAIL_PASSWORD = st.secrets["APP_SECRET_UFF_PASSWORD"]
APP_SECRET_UFF_RECEIVER = st.secrets["APP_SECRET_UFF_RECEIVER"]
APP_ANALISE= st.secrets["APP_ANALISE"]

# Config Session States
if 'check_email' not in st.session_state:
    if util.check_login(APP_SECRET_GMAIL, APP_SECRET_GMAIL_PASSWORD, HOST, PORT):
        st.session_state.check_email = True
    else:
        raise Exception("Erro ao validar o email, por favor entrar em contato com o administrador do sistema.")


# Configurar o modo wide
st.set_page_config(layout="wide", page_title="Avaliação LLM", page_icon='🤖')


CSV_FILE_ORIGIN = "data/fr0.csv"


# Função para carregar os textos a partir de um CSV
@st.cache_data
def load_texts():
    return pd.read_csv("data/fr0.csv")


# Função para selecionar dois textos aleatórios
def select_random_texts(df):
    pair = random.sample(df.index.tolist(), 2)
    return df.loc[pair[0]], df.loc[pair[1]]


# Título
st.title("Avaliação LLM 🤖")

df = pd.read_csv(CSV_FILE_ORIGIN)
fr = df['fr'][0]
# Instruções
st.markdown(f"""
### Bem-vindo!

O objetivo deste aplicativo é avaliar a qualidade de textos gerados por um modelo de linguagem.
Abaixo você encontrará dois textos gerados por modelos.
Leia os textos e responda as perguntas de avaliação.

Veja o fato relevante abaixo para entender de onde os textos foram gerados.

""")
with st.expander("Fato Relevante", expanded=True):
    st.write(f'''
        {fr}
    ''')


# Carrega os textos
textos_df = load_texts()

# Seleciona dois textos aleatórios
texto1, texto2 = select_random_texts(textos_df)

# Apresenta os textos
st.markdown("### Textos Selecionados")
col1, col2 = st.columns(2)

with col1:
    st.header("Análise 1")
    texto1["generated_text"] = texto1["generated_text"].replace("# ", "### ").replace("## ", "### ")
    st.markdown(texto1["generated_text"])

with col2:
    st.header("Análise 2")
    texto2["generated_text"] = texto2["generated_text"].replace("# ", "### ").replace("## ", "### ")
    st.markdown(texto2["generated_text"])

# Formulário para avaliação
st.markdown("### Avaliação")
with st.form("avaliacao_form"):
    st.write("Responda as perguntas abaixo:")
    
    resposta0 = st.radio("Alguma das análises apresentou informações incorretas ou inconsistentes em relação aos documentos financeiros analisados?", 
                         ["Nenhuma apresentou erro",
                          "A análise A apresentou erro", 
                          "A análise B apresentou erro", 
                          "Ambas apresentaram erros"]) 

    resposta1 = st.radio("Qual análise é mais fácil de compreender, considerando estrutura, linguagem e clareza?", 
                         ["Análise 1", 
                          "Análise 2", 
                          "Ambas têm o mesmo nível de clareza."]) 

    resposta2 = st.radio("Qual análise fornece as informações mais relevantes e aderentes ao fato relevante do documento?", 
                         ["Análise A", 
                          "Análise B", 
                          "Ambas são igualmente informativas"])

    resposta3 = st.radio("De maneira geral, qual análise você considera mais útil para a tomada de decisões?", 
                         ["Análise A", 
                          "Análise B", 
                          "Ambas igualmente úteis"])

    comentarios = st.text_area("Você gostaria de comentar algo sobre as análises apresentadas? (Opcional)")
    enviado = st.form_submit_button("Enviar")

    if enviado:
        
        # Adicionar os novos dados
        novo_dado = {
            "Texto 1": [texto1["generated_text"]],
            "Texto 2": [texto2["generated_text"]],
            "Resposta 0": [resposta0],
            "Resposta 1": [resposta1],
            "Resposta 2": [resposta2],
            "Resposta 3": [resposta3],
            "Comentários": [comentarios], 
        }

        df = pd.DataFrame(novo_dado)

        # Converter para CSV em memória
        csv_content = util.dataframe_para_csv(df)

        try:
            # Salvar os dados
            util.send_email(APP_SECRET_GMAIL, 
                            APP_SECRET_GMAIL_PASSWORD, 
                            "Avaliação LLM", 
                            APP_SECRET_UFF_RECEIVER, 
                            "Avaliação LLM", 
                            csv_content, 
                            'Data.csv', 
                            HOST, 
                            PORT)
            st.success("Respostas enviadas com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar os dados: {e}")
        
st.text(APP_ANALISE)