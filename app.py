import streamlit as st
import pandas as pd
import random
import os

# Configurar o modo wide
st.set_page_config(layout="wide", page_title="Avaliação LLM", page_icon='🤖')


# Nome do arquivo CSV onde os dados serão armazenados
CSV_FILE_ANSWERS = "data/respostas_usuarios.csv"
CSV_FILE_ORIGIN = "data/fr1.csv"

# Verifica se o arquivo existe, se não, cria com colunas padrão
if not os.path.exists(CSV_FILE_ANSWERS):
    pd.DataFrame(columns=["Texto 1", "Texto 2", "Resposta 1", "Resposta 2", "Resposta 3", "Comentários"]).to_csv(CSV_FILE_ANSWERS, index=True)


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

df = pd.read_csv(CSV_FILE_ORIGIN)
fr = df['fr'][0]
# Instruções
st.markdown(f"""
### Bem-vindo!

Abaixo você encontrará dois textos gerados por um modelo de linguagem.
Leia os textos e responda as perguntas de avaliação.

Veja o fato relevante abaixo:

""")
with st.expander("Fato Relevante"):
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
    st.markdown(texto1["generated_text"])

with col2:
    st.header("Análise 2")
    st.markdown(texto2["generated_text"])

# Formulário para avaliação
st.markdown("### Avaliação")
with st.form("avaliacao_form"):
    st.write("Responda as perguntas abaixo:")
    
    resposta0 = st.radio("Alguma das análises apresentou informações incorretas ou inconsistentes em relação aos documentos financeiros analisados?", ["Nenhuma apresentou erro","A análise A apresentou erro", "A análise B apresentou erro", "Ambas apresentaram erros"])

    resposta1 = st.radio("Qual análise é mais fácil de compreender, considerando estrutura, linguagem e clareza?", ["Análise 1", "Análise 2", "Ambas têm o mesmo nível de clareza."])

    resposta2 = st.radio("Qual análise fornece as informações mais relevantes e aderentes ao fato relevante do documento?", ["Análise A", "Análise B", "Ambas são igualmente informativas"])

    resposta3 = st.radio("De maneira geral, qual análise você considera mais útil para a tomada de decisões?", ["Análise A", "Análise B", "Ambas igualmente úteis"])

    comentarios = st.text_area("Você gostaria de comentar algo sobre as análises apresentadas? (Opcional)")
    enviado = st.form_submit_button("Enviar")

    if enviado:
        
        # Adicionar os novos dados
        novo_dado = {
            "Texto 1": texto1["generated_text"],
            "Texto 2": texto2["generated_text"],
            "Resposta 0": resposta0,
            "Resposta 1": resposta1,
            "Resposta 2": resposta2,
            "Resposta 3": resposta3,
            "Comentários": comentarios,
        }

        # novo_df = pd.DataFrame(novo_dado, index=[0])


        try:
            # Salvar os dados
            st.success("Respostas enviadas com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar os dados: {e}")
        
        st.success("Respostas enviadas com sucesso!")
