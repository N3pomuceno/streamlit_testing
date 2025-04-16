import random
from datetime import datetime

import pandas as pd
import streamlit as st

import src.util as util
from src.util_questions import RELEVANT_INFO

# import io
# import os

HOST = st.secrets["HOST"]
PORT = st.secrets["PORT"]
APP_SECRET_GMAIL = st.secrets["APP_SECRET_UFF_MAIL"]
APP_SECRET_GMAIL_PASSWORD = st.secrets["APP_SECRET_UFF_PASSWORD"]
APP_SECRET_UFF_RECEIVER = st.secrets["APP_SECRET_UFF_RECEIVER"]
APP_ANALISE = st.secrets["APP_ANALISE"]
CSV_FILE_ORIGIN = "data/m3_fr20_rankedModels.csv"
form_extent = RELEVANT_INFO["form_extent"]


# Função para carregar os textos a partir de um CSV
@st.cache_data
def load_df():
    return pd.read_csv(CSV_FILE_ORIGIN)


# Config Session States
def set_session_state():
    if "check_email" not in st.session_state:
        if util.check_login(APP_SECRET_GMAIL, APP_SECRET_GMAIL_PASSWORD, HOST, PORT):
            st.session_state.check_email = True
        else:
            raise Exception(
                "Erro ao validar o email, por favor entrar em contato com o administrador do sistema."
            )

    if "id" not in st.session_state:
        st.session_state.id = str(random.randint(0, 1000000)).zfill(
            6
        ) + datetime.now().strftime("%d_%m_%Y_%H%M")

    if "n_models" not in st.session_state:
        st.session_state.n_models = int(CSV_FILE_ORIGIN.split("/")[1].split("_")[0][1:])

    if "n_fr" not in st.session_state:
        st.session_state.n_fr = int(CSV_FILE_ORIGIN.split("/")[1].split("_")[1][2:])

    if "order" not in st.session_state:
        st.session_state.order = 0

    if "page_order" not in st.session_state:
        st.session_state.page_order = 0

    if "fr_order" not in st.session_state:
        st.session_state.fr_order = 0

    if "fr_model_order" not in st.session_state:
        st.session_state.fr_model_order = []

    if "analises" not in st.session_state:
        st.session_state.analises = {}

    if "most_liked_analysis_defined" not in st.session_state:
        st.session_state.most_liked_analysis_defined = False

    if "extent" not in st.session_state:
        st.session_state.extent = False

    return None


# Configurar o modo wide
def set_page_config():
    st.set_page_config(layout="wide", page_title="Avaliação LLM", page_icon="🤖")


def select_texts(analises_dict):
    keys = list(analises_dict.keys())[:2]
    return analises_dict[keys[0]], analises_dict[keys[1]]


# Função para avançar para a próxima página
def next_page():
    st.session_state.order += 1
    return None


def run_app():
    # Título
    st.title("Avaliação LLM 🤖")

    if st.session_state.order == 0:
        st.markdown("""### Instruções
                    
                    Adicionar Texto.""")
        st.session_state.extent = st.checkbox("Avaliação Extendida", value=False)
        st.button("Avançar", key="button1", on_click=next_page)
    elif st.session_state.n_fr == st.session_state.fr_model_order:
        st.markdown(
            """
                    ### Você avaliou todos os textos!
                    Obrigado por Participar!

                    Para maiores informações, entre em contato com o administrador do sistema."""
        )
    else:
        # Carrega o CSV e define o fato relevante
        df = load_df()
        df_temp = df[df["new_id"] == st.session_state.fr_order]

        # Carrega os textos, cria dicionário para manter informações conectadas, e lista para definir ordem de aparecimento.
        for _, row in df_temp.iterrows():
            st.session_state.analises[row["generator_model"]] = row["generated_text"]
        st.session_state.analises["human_ref"] = df_temp["human_ref"].iloc[0]
        # Define uma lista com ordem dos modelos baseado na coluna total_rank e por último o humano
        if len(st.session_state.fr_model_order) == 0:
            order = list(df_temp["generator_model"].unique())
            order.reverse()
            order.append("human_ref")
            st.session_state.fr_model_order = order
            # Ordem definida, precisa fazer a passagem de duas formas, entre comparação de duas colunas, e algo fazendo continuamente para todos.

        fr = df_temp["material fact"].iloc[0]

        # Instruções
        st.markdown(
            """
        ### Bem-vindo!

        O objetivo deste aplicativo é avaliar a qualidade de textos gerados por um modelo de linguagem.
        Abaixo você encontrará análises gerados por modelos.
        Leia-os e responda as perguntas de avaliação.

        Veja o fato relevante abaixo para entender de onde os textos foram gerados.

        """
        )
        with st.expander("Fato Relevante", expanded=True):
            st.write(
                f"""
                {fr}
            """
            )

        if st.session_state.extent or st.session_state.most_liked_analysis_defined:
            if st.session_state.extent:
                generated_text = st.session_state.analises[
                    st.session_state.fr_model_order[st.session_state.page_order]
                ]
            else:
                generated_text = st.session_state.analises[
                    st.session_state.fr_model_order[0]
                ]

            text = generated_text.replace("# ", "### ").replace("## ", "### ")
            st.markdown(text)

            # Formulário para avaliação
            st.markdown("## Avaliação")
            with st.form("avaliacao_form", clear_on_submit=True):
                st.markdown(RELEVANT_INFO["texts"]["form_extent_intro"])
                st.markdown(form_extent["question0"]["question"])

                resposta0 = st.pills(
                    "Fluência",
                    options=form_extent["question0"]["options"],
                    key="Fluência",
                    help="1 - Muito ruim, 2 - Ruim, 3 - Regular, 4 - Bom, 5 - Muito bom",
                    label_visibility="collapsed",
                )

                st.markdown(form_extent["question1"]["question"])

                resposta1 = st.pills(
                    "Coerência",
                    options=form_extent["question1"]["options"],
                    key="Coerência",
                    help="1 - Muito ruim, 2 - Ruim, 3 - Regular, 4 - Bom, 5 - Muito bom",
                    label_visibility="collapsed",
                )

                st.markdown(form_extent["question2"]["question"])
                resposta2 = st.pills(
                    "Factualidade",
                    options=form_extent["question2"]["options"],
                    key="Factualidade",
                    help="1 - Muito ruim, 2 - Ruim, 3 - Regular, 4 - Bom, 5 - Muito bom",
                    label_visibility="collapsed",
                )

                st.markdown(form_extent["question3"]["question"])
                resposta3 = st.pills(
                    "Aderência",
                    options=form_extent["question3"]["options"],
                    key="Aderência",
                    help="1 - Muito ruim, 2 - Ruim, 3 - Regular, 4 - Bom, 5 - Muito bom",
                    label_visibility="collapsed",
                )

                st.markdown(form_extent["question4"]["question"])

                resposta4 = st.pills(
                    "Utilidade",
                    options=form_extent["question4"]["options"],
                    key="Utilidade",
                    help="1 - Muito ruim, 2 - Ruim, 3 - Regular, 4 - Bom, 5 - Muito bom",
                    label_visibility="collapsed",
                )

                st.markdown(form_extent["comentarios0"]["question"])

                comentarios0 = st.text_area(
                    "Comentarios Finais",
                    key="comentarios",
                    label_visibility="collapsed",
                )

                enviado = st.form_submit_button("Enviar")

                if enviado:
                    # Prepara para próxima página
                    st.session_state.page_order += 1
                    if st.session_state.page_order >= st.session_state.n_models + 1:
                        st.session_state.fr_order += 1
                        st.session_state.page_order = 0

                    if st.session_state.most_liked_analysis_defined:
                        st.session_state.most_liked_analysis_defined = False

                    generator_model = st.session_state.fr_model_order[
                        st.session_state.page_order
                    ]

                    # Preparar novos dados para serem recebidos;
                    novo_dado = {
                        "text": [text],
                        "material_fact": [fr],
                        "generator_model": generator_model,
                        "answer0": [resposta0],
                        "answer1": [resposta1],
                        "answer2": [resposta2],
                        "answer3": [resposta3],
                        "answer4": [resposta4],
                        "sugestions": [comentarios0],
                    }

                    df_answer = pd.DataFrame(novo_dado)

                    # Converter para CSV em memória
                    csv_content = util.dataframe_para_csv(df_answer)

                    try:
                        # # Salvar os dados
                        # util.send_email(
                        #     usn=APP_SECRET_GMAIL,
                        #     pwd=APP_SECRET_GMAIL_PASSWORD,
                        #     sub="Avaliação LLM: {}".format(st.session_state.id),
                        #     to=APP_SECRET_UFF_RECEIVER,
                        #     body="Avaliação LLM: doc {} \n generator_model {}".format(
                        #         st.session_state.fr_model_order, generator_model
                        #     ),
                        #     csv_content=csv_content,
                        #     filename="data.csv",
                        #     host=HOST,
                        #     port=PORT,
                        # )
                        st.success(
                            "Respostas enviadas com sucesso! Por favor retorne ao início da página, para ver a próxima avaliação."
                        )
                    except Exception as e:
                        st.error(
                            f"Erro ao salvar os dados: {e}. Por favor entrar em contato com os responsáveis pela atividade."
                        )
        else:
            # Definir as duas análises por ordem da lista
            texto1, texto2 = select_texts(st.session_state.analises)

            # Preparar textos e definir as colunas
            col1, col2 = st.columns(2)

            with col1:
                st.header("Análise A")
                texto1 = texto1.replace("# ", "### ").replace("## ", "### ")
                st.markdown(texto1)

            with col2:
                st.header("Análise B")
                texto2 = texto2.replace("# ", "### ").replace("## ", "### ")
                st.markdown(texto2)

            # Formulário para avaliação
            st.markdown("## Avaliação")
            with st.form("form_most_liked", clear_on_submit=True):
                st.markdown("#### Qual análise você mais gostou? (Selecione uma opção)")
                resposta0 = st.selectbox(
                    "Selecione uma opção",
                    options=["Análise A", "Análise B"],
                    key="most_liked",
                    label_visibility="collapsed",
                )
                enviado = st.form_submit_button("Enviar")

                if enviado:
                    # Prepara para próxima página
                    st.session_state.page_order += 1
                    if resposta0 == "Análise A":
                        # Retira o outro texto da lista
                        st.session_state.analises.pop(
                            st.session_state.fr_model_order[1]
                        )
                        st.session_state.fr_model_order.pop(1)
                    elif resposta0 == "Análise B":
                        # Retira o outro texto da lista
                        st.session_state.analises.pop(
                            st.session_state.fr_model_order[0]
                        )
                        st.session_state.fr_model_order.pop(0)
                    if len(st.session_state.fr_model_order) == 1:
                        st.session_state.most_liked_analysis_defined = True


def main():
    # Configuração do Streamlit
    set_session_state()
    # Configuração da página
    set_page_config()
    # Execução do aplicativo
    run_app()


if __name__ == "__main__":
    main()
