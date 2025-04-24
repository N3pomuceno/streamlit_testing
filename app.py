import random
from datetime import datetime

import pandas as pd
import streamlit as st

import src.util as util
from src.util_texts import RELEVANT_INFO

# from src.logger import setup_logger

# import io
# import os

HOST = st.secrets["HOST"]
PORT = st.secrets["PORT"]
APP_SECRET_GMAIL = st.secrets["APP_SECRET_UFF_MAIL"]
APP_SECRET_GMAIL_PASSWORD = st.secrets["APP_SECRET_UFF_PASSWORD"]
APP_SECRET_UFF_RECEIVER = st.secrets[
    "APP_SECRET_TEST_RECEIVER"
]  # APP_SECRET_UFF_RECEIVER"]
CSV_FILE_ORIGIN = st.secrets["CSV_FILE_ORIGIN"]
form_extent = RELEVANT_INFO["form_extent"]
# logger = setup_logger("logs", "app.log", "INFO")


def init_session_state_var(key, default_value):
    """
    Inicializa uma variável de estado da sessão se ela não existir.
    """
    # logger.info("Inicializando variável de estado da sessão: {}".format(key))
    if key not in st.session_state:
        st.session_state[key] = default_value


# Config Session States
def set_session_state():
    """
    Inicia as variáveis de estado da sessão.
    """
    # Valida e-mail
    if "check_email" not in st.session_state:
        if util.check_login(APP_SECRET_GMAIL, APP_SECRET_GMAIL_PASSWORD, HOST, PORT):
            st.session_state.check_email = True
        else:
            raise Exception(
                "Erro ao validar o email, por favor entrar em contato com o administrador do sistema."
            )
    # Define um ID único para a sessão
    init_session_state_var(
        "id",
        "{}-{}".format(
            str(random.randint(0, 1000000)).zfill(6),
            datetime.now().strftime("%d_%m_%Y_%H%M"),
        ),
    )
    # Define a quantidade de modelos e de fatos relevantes baseado no nome do arquivo CSV
    init_session_state_var(
        "n_models", int(CSV_FILE_ORIGIN.split("/")[1].split("_")[0][1:])
    )
    init_session_state_var("n_fr", int(CSV_FILE_ORIGIN.split("/")[1].split("_")[1][2:]))

    # Define ordens de estágio da atividade, da quantidade de modelos e de fatos relevantes respectivamente
    init_session_state_var("order", 0)
    init_session_state_var("page_order", 0)
    init_session_state_var("fr_order", 0)

    # Define uma lista com a ordem de modelos que serão apresentados e um dicionário com as análises
    init_session_state_var("fr_model_order", [])
    init_session_state_var("analises", {})

    # Define o estado da avaliação para o caso de analisar em dupla
    init_session_state_var("most_liked_analysis_defined", False)
    init_session_state_var("most_liked_order", "")

    # Define o estado da avaliação para o caso de avaliar em grão mais fino.
    init_session_state_var("extent", False)

    # Define o estado do formulário e também o estado das questões.
    init_session_state_var("form_submitted", False)
    init_session_state_var("most_liked", None)
    return None


set_session_state()


# Função para carregar os textos a partir de um CSV
@st.cache_data
def load_df():
    """
    Retorna um DataFrame a partir de um arquivo CSV.
    O arquivo CSV deve conter as colunas 'generator_model', 'generated_text' e 'human_ref'.
    """
    return pd.read_csv(CSV_FILE_ORIGIN)


# Configurar o modo wide
def set_page_config():
    # logger.info("Configurando o layout da página")
    st.set_page_config(layout="wide", page_title="Avaliação LLM", page_icon="🤖")


# Função para selecionar os textos a serem exibidos
def select_texts(analises_dict, analises_order):
    keys = analises_order[:2]
    return analises_dict[keys[0]], analises_dict[keys[1]]


# Função para avançar para a próxima página
def next_page():
    st.session_state.order += 1
    return None


# Callback do botão — só marca que o botão foi clicado do formulário.
def form_callback():
    st.session_state["form_submitted"] = True


def load_data():
    # logger.info(
    #     "Carregando dados do CSV e definindo os dados temporários por ordem, fato relevante atual: {}".format(
    #         st.session_state.fr_order
    #     )
    # )
    # Carrega o CSV e define o fato relevante
    df = load_df()
    df_temp = df[df["new_id"] == st.session_state.fr_order]

    # Carrega os textos, cria dicionário para manter informações conectadas, e lista para definir ordem de aparecimento.
    if len(st.session_state.analises) == 0:
        for _, row in df_temp.iterrows():
            st.session_state.analises[row["generator_model"]] = row["generated_text"]
        st.session_state.analises["human_ref"] = df_temp["human_ref"].iloc[0]
        print("Novas análises definidas: {}".format(st.session_state.analises.keys()))

    # Define uma lista com ordem dos modelos baseado na coluna total_rank e por último o humano
    if len(st.session_state.fr_model_order) == 0:
        order = list(df_temp["generator_model"].unique())
        order.reverse()
        order.append("human_ref")
        st.session_state.fr_model_order = order
        print("Nova ordem estabelecida: {}".format(order))

    # Define o Fato Relevante que será apresentado
    st.session_state["material_fact"] = df_temp["material fact"].iloc[0]

    return None


# TODO Alterar para alterar a lista de acordo com os fato relevantes forem sendo definidos.
if st.session_state["form_submitted"]:
    st.session_state.page_order += 1
    if st.session_state.extent or st.session_state.most_liked_analysis_defined:
        if len(st.session_state.fr_model_order) == 0:
            st.session_state.fr_order += 1
            st.session_state.page_order = 0
        else:
            st.session_state.fr_model_order.pop(0)

        if st.session_state.most_liked_analysis_defined:
            st.session_state.most_liked_analysis_defined = False
            st.session_state.most_liked_order = ""
    else:
        # Prepara para próxima página
        print("Resposta = {}".format(st.session_state.most_liked))
        if st.session_state.most_liked == "Análise A":
            indice = 1
        elif st.session_state.most_liked == "Análise B":
            indice = 0
        print("Excluindo modelo {}".format(st.session_state.fr_model_order[indice]))
        st.session_state.most_liked_order = "{} > {}".format(
            st.session_state.most_liked_order, st.session_state.fr_model_order[indice]
        )
        # Retira o outro texto da lista
        st.session_state.analises.pop(st.session_state.fr_model_order[indice])
        st.session_state.fr_model_order.pop(indice)
        print("Modelos Restantes: {}".format(st.session_state.fr_model_order))
        if len(st.session_state.fr_model_order) == 1:
            st.session_state.most_liked_analysis_defined = True
            print("Definindo a análise mais gostada.")
    st.session_state["form_submitted"] = False


# Funções para mostrar as páginas
def show_intro_page():
    pass


def show_finishing_page():
    pass


def show_comparing_page():
    pass


def show_evaluation_page():
    pass


def show_interface():
    # Título
    st.title("Avaliação LLM 🤖")

    if st.session_state.order == 0:
        show_intro_page()
        st.markdown("""
                    ### Bem-vindo(a)!

                    Este formulário tem como objetivo coletar avaliações de diferentes análises sobre documentos financeiros específicos. A sua participação é fundamental para compreendermos a percepção sobre a qualidade das análises produzidas com base em critérios como fluência textual, factualidade e coerência argumentativa entre outros.

                    Você poderá escolher entre dois formatos de avaliação:

                    #### **Avaliação Comparativa Simples**

                    Nesta opção, você irá comparar as análises disponíveis e escolher aquela que mais se destaca em sua opinião. Em seguida, você fará uma avaliação detalhada apenas dessa análise escolhida.

                    #### **Avaliação Detalhada de Todas as Análises**

                    Nesta opção, você realizará uma avaliação individual e aprofundada de todas as análises disponíveis, atribuindo notas ou comentários sobre aspectos como fluência, precisão dos dados, estrutura argumentativa, entre outros. Para escolher essa opção, você deve estar ciente de que a avaliação será mais extensa e exigirá mais tempo. Caso tenha interesse nela, basta marcar a opção abaixo.

                    ##### ⚠️ A escolha do formato de avaliação impacta na quantidade de horas complementares que serão atribuídas!

                    Escolha o formato que melhor se encaixa na sua disponibilidade e interesse. Em qualquer dos casos, sua participação é muito valiosa para o projeto.
                    
                    ---
                    """)
        st.session_state.extent = st.checkbox("Avaliação Detalhada", value=False)
        st.button("Avançar", key="button1", on_click=next_page)
    elif st.session_state.n_fr == st.session_state.fr_model_order:  # Last Page
        show_finishing_page()
        st.markdown(
            """
            ✅ Avaliação Concluída!

            Obrigado pela sua participação!

            Sua avaliação foi registrada com sucesso. Agradecemos por contribuir com a análise crítica das interpretações de documentos financeiros — sua colaboração é essencial para o desenvolvimento de iniciativas acadêmicas e de pesquisa na área.
            """
        )
    else:
        fr = st.session_state.material_fact
        fr = fr.replace("$", r"\$")
        # Instruções da Atividade
        st.markdown(
            """
        ### Bem-vindo!

        ###### Este aplicativo tem como objetivo avaliar a qualidade das análises apresentadas com base em um documento financeiro.

        ##### ✅ Siga os passos abaixo:

        Leia o fato relevante apresentado abaixo.
        Ele é a base para todas as análises que você verá a seguir.

        Responda o formulário ao final da página.
        O tipo de formulário exibido dependerá do formato de avaliação que você escolheu anteriormente.

        🕒 Lembre-se de sempre responder os formulários no final.

        """
        )

        # Progresso Visual para o usuário.
        st.progress(
            (st.session_state.fr_order + 1) / st.session_state.n_fr,
            text="Fato Relevante: {}/{}".format(
                st.session_state.fr_order + 1, st.session_state.n_fr
            ),
        )

        # Fato Relevante para o usuário Visualizar
        with st.expander("Fato Relevante", expanded=True):
            st.write(
                f"""
                {fr}
            """
            )

        # Verifica se é a avaliação em grão mais fino ou se é o último caso da avaliação de comparação
        if st.session_state.extent or st.session_state.most_liked_analysis_defined:
            print(st.session_state.fr_model_order)
            generator_model = st.session_state.fr_model_order[0]
            generated_text = st.session_state.analises[generator_model]
            print("Modelo: {}".format(generator_model))

            # Verifica se é o último modelo ou se é a versão de validar em par para reiniciar os modelos.
            if (
                st.session_state.most_liked_analysis_defined
                or st.session_state.page_order == st.session_state.n_models
            ):
                st.session_state.analises = {}
                st.session_state.fr_model_order = []

            text = (
                generated_text.replace("# ", "### ")
                .replace("## ", "### ")
                .replace("$", r"\$")
            )
            st.markdown(text)

            # Formulário para avaliação
            st.markdown("## Avaliação")
            with st.form("avaliacao_form", clear_on_submit=False):
                st.markdown(RELEVANT_INFO["texts"]["form_extent_intro"])
                st.markdown(form_extent["question0"]["question"])

                resposta0 = st.pills(
                    "Fluência",
                    options=form_extent["question0"]["options"],
                    key="fluencia",
                    help="1 - Muito ruim, 2 - Ruim, 3 - Regular, 4 - Bom, 5 - Muito bom",
                    label_visibility="collapsed",
                )

                st.markdown(form_extent["question1"]["question"])

                resposta1 = st.pills(
                    "Coerência",
                    options=form_extent["question1"]["options"],
                    key="coerencia",
                    help="1 - Muito ruim, 2 - Ruim, 3 - Regular, 4 - Bom, 5 - Muito bom",
                    label_visibility="collapsed",
                )

                st.markdown(form_extent["question2"]["question"])
                resposta2 = st.pills(
                    "factualidade",
                    options=form_extent["question2"]["options"],
                    key="Factualidade",
                    help="1 - Muito ruim, 2 - Ruim, 3 - Regular, 4 - Bom, 5 - Muito bom",
                    label_visibility="collapsed",
                )

                st.markdown(form_extent["question3"]["question"])
                resposta3 = st.pills(
                    "aderencia",
                    options=form_extent["question3"]["options"],
                    key="Aderência",
                    help="1 - Muito ruim, 2 - Ruim, 3 - Regular, 4 - Bom, 5 - Muito bom",
                    label_visibility="collapsed",
                )

                st.markdown(form_extent["question4"]["question"])

                resposta4 = st.pills(
                    "utilidade",
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

                enviado = st.form_submit_button("Enviar", on_click=form_callback)

                if enviado:
                    novo_dado = {
                        "id": [st.session_state.id],
                        "text": [text],
                        "material_fact": [fr],
                        "generator_model": generator_model,
                        "answer0": [resposta0],
                        "answer1": [resposta1],
                        "answer2": [resposta2],
                        "answer3": [resposta3],
                        "answer4": [resposta4],
                        "sugestions": [comentarios0],
                        "most_liked_order": [st.session_state.most_liked_order],
                    }

                    df_answer = pd.DataFrame(novo_dado)

                    # Converter para CSV em memória
                    csv_content = util.dataframe_para_csv(df_answer)

                    try:
                        # # Salvar os dados
                        util.send_email(
                            usn=APP_SECRET_GMAIL,
                            pwd=APP_SECRET_GMAIL_PASSWORD,
                            sbj="Avaliação LLM: {} - {}/{}".format(
                                st.session_state.id,
                                st.session_state.fr_order + 1,
                                st.session_state.n_fr,
                            ),
                            to=APP_SECRET_UFF_RECEIVER,
                            body="Avaliação LLM: \n Grão fino: {} \n Modelo Gerador: {} \n Ordem que mais gostou: {}".format(
                                st.session_state.extent,
                                generator_model,
                                st.session_state.most_liked_order,
                            ),
                            csv_content=csv_content,
                            filename="data.csv",
                            host=HOST,
                            port=PORT,
                        )
                        st.success(
                            "Respostas enviadas com sucesso! Por favor retorne ao início da página, para ver a próxima avaliação."
                        )
                    except Exception as e:
                        st.error(
                            f"Erro ao salvar os dados: {e}. Por favor entrar em contato com os responsáveis pela atividade."
                        )
        else:
            # Definir as duas análises por ordem da lista
            print(
                "Hora da análise: {} - {}".format(
                    st.session_state.fr_model_order, st.session_state.fr_model_order[0]
                )
            )
            texto1, texto2 = select_texts(
                st.session_state.analises, st.session_state.fr_model_order
            )

            # Preparar textos e definir as colunas
            col1, col2 = st.columns(2)

            with col1:
                st.header("Análise A")
                texto1 = (
                    texto1.replace("# ", "### ")
                    .replace("## ", "### ")
                    .replace("$", r"\$")
                )
                print(
                    "{} - {}".format(
                        st.session_state.fr_model_order,
                        st.session_state.fr_model_order[0],
                    )
                )
                st.markdown(texto1)

            with col2:
                st.header("Análise B")
                texto2 = (
                    texto2.replace("# ", "### ")
                    .replace("## ", "### ")
                    .replace("$", r"\$")
                )
                print(
                    "{} - {}".format(
                        st.session_state.fr_model_order,
                        st.session_state.fr_model_order[1],
                    )
                )
                st.markdown(texto2)

            # Formulário para avaliação
            st.markdown("## Avaliação")
            with st.form("form_most_liked", clear_on_submit=True):
                st.markdown("#### Qual análise você mais gostou? (Selecione uma opção)")
                resposta0 = st.pills(
                    "Selecione uma opção",
                    options=["Análise A", "Análise B"],
                    key="most_liked",
                    label_visibility="collapsed",
                )
                enviado = st.form_submit_button("Enviar", on_click=form_callback)


def main():
    # Configuração do Streamlit
    set_page_config()

    # Carregar dados
    load_data()

    # Execução do aplicativo
    show_interface()


if __name__ == "__main__":
    main()
