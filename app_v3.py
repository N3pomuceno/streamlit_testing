import logging
import random
import re
from datetime import datetime

import pandas as pd
import streamlit as st

import src.util as util
from src.util_texts import RELEVANT_INFO

logging.basicConfig(
    format="%(asctime)s %(levelname)s [%(filename)s]:%(lineno)d - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# import io
# import os

HOST = st.secrets["HOST"]
PORT = st.secrets["PORT"]
APP_SECRET_GMAIL = st.secrets["APP_SECRET_UFF_MAIL"]
APP_SECRET_GMAIL_PASSWORD = st.secrets["APP_SECRET_UFF_PASSWORD"]
APP_SECRET_UFF_RECEIVER = st.secrets["APP_SECRET_UFF_RECEIVER"]
CSV_FILE_ORIGIN = st.secrets["CSV_FILE_ORIGIN"]
form_extent = RELEVANT_INFO["form_extent"]


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
        logger.info(
            "Novas análises definidas: {}".format(st.session_state.analises.keys())
        )

    # Define uma lista com ordem dos modelos baseado na coluna total_rank e por último o humano
    if len(st.session_state.fr_model_order) == 0:
        order = list(df_temp["generator_model"].unique())
        order.reverse()
        order.append("human_ref")
        st.session_state.fr_model_order = order
        logger.info("Nova ordem estabelecida: {}".format(order))

    # Define o Fato Relevante que será apresentado
    st.session_state["material_fact"] = df_temp["material fact"].iloc[0]

    return None


def remover_elementos_markdown(texto_markdown):
    """
    Remove cabeçalhos Markdown, negrito, cabeçalhos <> e linhas
    que contêm apenas texto em negrito.

    Args:
        texto_markdown: Uma string contendo o texto em Markdown.

    Returns:
        Uma string com os elementos especificados removidos.
    """

    # 1. Remover cabeçalhos segmentados por <>
    texto_processado = re.sub(r"<[^>]+>", "", texto_markdown)

    # 2. Remover linhas que contêm APENAS negrito (e possíveis espaços)
    # Procura por linhas que:
    #   ^        - começam no início da linha
    #   \s* - podem ter espaços em branco
    #   \*\*.*?\*\* - contêm texto em negrito (**)
    #   \s* - podem ter espaços em branco depois
    #   $        - terminam no fim da linha
    # Substitui a linha inteira por uma string vazia. Usa re.MULTILINE.
    texto_processado = re.sub(
        r"^\s*\*\*(.*?)\*\*\s*$", "", texto_processado, flags=re.MULTILINE
    )
    # Faz o mesmo para o negrito com __ (underscore)
    texto_processado = re.sub(
        r"^\s*__(.*?)__\s*$", "", texto_processado, flags=re.MULTILINE
    )

    # 3. Remover formatação de negrito restante (em linhas com outro texto)
    # Agora, remove apenas os marcadores de negrito das linhas que sobraram.
    texto_processado = re.sub(r"\*\*(.*?)\*\*", r"\1", texto_processado)
    texto_processado = re.sub(r"__(.*?)__", r"\1", texto_processado)

    # 4. Remover cabeçalhos padrão (#, ##, etc.)
    texto_processado = re.sub(r"^#+\s+.*$", "", texto_processado, flags=re.MULTILINE)

    # 5. Limpar linhas em branco excessivas
    # Remove linhas que ficaram completamente vazias ou só com espaços.
    texto_processado = re.sub(r"^\s*$", "", texto_processado, flags=re.MULTILINE)
    # Garante que não haja mais de duas quebras de linha seguidas.
    texto_processado = re.sub(r"\n{3,}", "\n\n", texto_processado)
    # Remove espaços em branco no início e fim.
    texto_processado = texto_processado.strip()

    return texto_processado


def caracteristicas_texto(key: str) -> dict:
    """
    Função da interface que mostrará as checkboxes para o usuário avaliar os textos.
    """
    resposta = {}
    # Cria as checkboxes para o usuário avaliar os textos
    st.markdown(
        """
        ## Em quais aspectos esse texto se destaca? 
        Lembre-se que se deixar todos os campos em branco, implicará dizer que o texto não se destaca em nenhum aspecto."""
    )
    resposta["factuality"] = st.checkbox(
        "Factualidade",
        key="factuality_{}".format(key),
        help="As informações fornecidas pelo texto são verdadeiras e baseadas em fatos verificáveis, mesmo que não tenham sido citados no fato relevante? Um texto que apresenta dados falsos ou distorcidos tem baixa factualidade. Caso as informações tenham sido inventadas (ou alucinadas) a factualidade é baixa.",
    )
    resposta["usefulness"] = st.checkbox(
        "Utilidade",
        key="usefulness_{}".format(key),
        help="Quanto o texto é útil, informativo e contribui de forma concreta para o entendimento ou a tomada de decisão? Um conteúdo com alta utilidade apresenta informações específicas, relevantes e com valor agregado. Um relatório que apresenta dados objetivos, análises detalhadas e implicações diretas para os acionistas demonstra alta utilidade. Um relatório que traz apenas opiniões vagas, frases genéricas ou observações evidentes (como “a empresa busca sempre crescer”) tem baixa utilidade. De maneira geral, qual análise você considera mais útil para a tomada de decisões?",
    )
    resposta["simplicity"] = st.checkbox(
        "Simplicidade",
        key="simplicity_{}".format(key),
        help="Um texto simples contém linguagem acessível e clara, evitando termos técnicos ou explicando-os quando necessários, de modo que qualquer leitor, mesmo sem formação na área econômica, consiga compreender as informações e argumentos apresentados.",
    )
    resposta["objectivity"] = st.checkbox(
        "Objetividade",
        key="objectivity_{}".format(key),
        help="O texto apresenta informações e argumentos de forma clara, direta e fundamentada, evitando opiniões vagas? Evita juízos de valor infundados, termos sensacionalistas ou especulações sem base? Acrescenta uma camada analítica, oferecendo interpretações consistentes e bem embasadas, com base em indicadores, cenários econômicos ou tendências de mercado?  Ou limita-se a reproduzir os fatos reportados no fato relevante, mesmo que o faça de forma explicativa e clara?",
    )
    resposta["confiability"] = st.checkbox(
        "Confiabilidade/Parcialidade",
        key="confiability_{}".format(key),
        help="O texto apresenta dados e fatos de forma neutra, contextualizando-os corretamente e sem distorções? Menciona fontes confiáveis (relatórios oficiais, indicadores econômicos, declarações verificáveis)? Evita viés político, ideológico ou institucional que possa comprometer a análise? Não omite informações relevantes que poderiam alterar a compreensão do leitor sobre o tema?",
    )

    resposta["reason"] = st.text_input(
        "Quais é o motivo para você definir esses aspectos?",
        key="reason_{}".format(key),
    )
    return resposta


if st.session_state["form_submitted"]:
    st.session_state.page_order += 1

    # Prepara para próxima página
    if (
        len(st.session_state.fr_model_order) != 1
        and not st.session_state.most_liked_analysis_defined
    ):
        logger.info("Resposta = {}".format(st.session_state.most_liked))
        if st.session_state.most_liked == "Análise A":
            indice = 1
        elif st.session_state.most_liked == "Análise B":
            indice = 0

        # Ordem os textos de acordo com a avaliação do usuário
        st.session_state.most_liked_order = "{} > {}".format(
            st.session_state.most_liked_order, st.session_state.fr_model_order[indice]
        )
    else:
        indice = 0

    if len(st.session_state.fr_model_order) == 1 and st.session_state.extent:
        novo_dado = {
            "id": [st.session_state.id],
            "text": [st.session_state.analises[st.session_state.fr_model_order[0]]],
            "material_fact": [st.session_state.material_fact],
            "generator_model": st.session_state.fr_model_order[0],
            "factuality": [
                "Se destaca"
                if st.session_state["factuality_{}".format(st.session_state.fr_order)]
                else "Não se destaca"
            ],
            "usefulness": [
                "Se destaca"
                if st.session_state["usefulness_{}".format(st.session_state.fr_order)]
                else "Não se destaca"
            ],
            "simplicity": [
                "Se destaca"
                if st.session_state["simplicity_{}".format(st.session_state.fr_order)]
                else "Não se destaca"
            ],
            "objectivity": [
                "Se destaca"
                if st.session_state["objectivity_{}".format(st.session_state.fr_order)]
                else "Não se destaca"
            ],
            "confiability": [
                "Se destaca"
                if st.session_state["confiability_{}".format(st.session_state.fr_order)]
                else "Não se destaca"
            ],
            "reason": [st.session_state["reason_{}".format(st.session_state.fr_order)]],
            "most_liked_order": [st.session_state.most_liked_order],
        }

        df_answer = pd.DataFrame(novo_dado)

        # Converter para CSV em memória
        csv_content = util.dataframe_para_csv(df_answer)

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
                st.session_state.fr_model_order[0],
                st.session_state.most_liked_order,
            ),
            csv_content=csv_content,
            filename="data.csv",
            host=HOST,
            port=PORT,
        )
    # Retira o outro texto da lista
    st.session_state.analises.pop(st.session_state.fr_model_order[indice])
    st.session_state.fr_model_order.pop(indice)
    # Caso sobre somente uma última análise, define a análise mais gostada
    if len(st.session_state.fr_model_order) == 1:
        st.session_state.most_liked_analysis_defined = True
        st.session_state.most_liked_order = "{} > {}".format(
            st.session_state.most_liked_order, st.session_state.fr_model_order[0]
        )
        if not st.session_state.extent:
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
                    "Comparativo Simples",
                    st.session_state.fr_model_order[0],
                    st.session_state.most_liked_order,
                ),
                host=HOST,
                port=PORT,
            )
            st.session_state.analises.pop(st.session_state.fr_model_order[0])
            st.session_state.fr_model_order.pop()
    if len(st.session_state.fr_model_order) == 0:
        st.session_state.most_liked_analysis_defined = False
        st.session_state.most_liked_order = ""
        st.session_state.fr_order += 1
        st.session_state.analises = {}
    st.session_state["form_submitted"] = False


def show_interface():
    # Título
    st.title("Avaliação LLM 🤖")

    if st.session_state.order == 0:
        st.markdown("""
                    ### Bem-vindo(a)!

        Esse formulário é parte de uma pesquisa científica para entender a qualidade de análises de documentos financeiros geradas por inteligência artificial.

        Este formulário tem como objetivo coletar avaliações de diferentes análises sobre documentos financeiros específicos. A sua participação é fundamental para compreendermos a percepção sobre a qualidade das análises produzidas com base em critérios como fluência textual, factualidade e coerência argumentativa, entre outros.
        Para nos ajudar nessa pesquisa, você, que já tem familiaridade com esse tipo de conteúdo, vai avaliar duas análises sobre o mesmo documento.

        Você poderá escolher entre dois formatos de avaliação:

        #### **Avaliação Comparativa Simples**

        Nesta opção, você irá ler um “fato relevante” e, em seguida, comparar duasas análises disponíveis sobre este fato. Então, você irá e escolher a melhor análiseaquela que mais se destaca em sua opinião. Em seguida, você fará uma avaliação detalhada apenas dessa análise escolhida.

        #### **Avaliação Detalhada de Todas as Análises**

        Ao optar por participar da avaliação detalhada, além de escolher a melhor análise, você irá detalhar porquê escolheu determinada análise. Aqui você poderá avaliar critérios como 
        Nesta opção, você realizará uma avaliação individual e aprofundada de todas as análises disponíveis, atribuindo notas ou comentários sobre aspectos como fluência e, precisão dos dados, também poderá incluir seu próprio critérioestrutura argumentativa, entre outros.Ao Para escolher essa opção, você deve estar ciente de que a avaliação será mais extensa e exigirá mais tempo. Você estará ajudando não apenas a entender a habilidade de inteligências artificias para o domínio financeiro, mas também estará indicando o que precisamos melhorar. Caso tenha interesse nela, basta marcar a opção abaixo.

        ##### ⚠️ A escolha do formato de avaliação impacta na quantidade de horas complementares que serão atribuídas!

        Escolha o formato que melhor se encaixa na sua disponibilidade e interesse. Em qualquer dos casos, sua participação é muito valiosa para o projeto.
                    """)
        st.session_state.extent = st.checkbox("Avaliação Detalhada", value=False)
        st.button("Avançar", key="button1", on_click=next_page)
    elif st.session_state.n_fr == st.session_state.fr_model_order:  # Last Page
        st.markdown(
            """
        ✅ Avaliação Concluída!

        Agradecemos a sua participação!

        Sua avaliação foi registrada com sucesso. Valorizamos sua contribuiçãocom a análise crítica das interpretações de documentos financeiros — sua colaboração é essencial para o desenvolvimento de iniciativas acadêmicas e de pesquisa na área.

            """
        )
    else:
        fr = st.session_state.material_fact
        fr = fr.replace("$", r"\$")
        # Instruções da Atividade
        st.markdown(
            """
            ### Bem-vindo!

            ###### Este aplicativo tem como objetivo avaliar a qualidade das análises apresentadas com base em um fato relevante.

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

        logger.info(
            "{} - {}".format(
                st.session_state.extent, st.session_state.most_liked_analysis_defined
            )
        )

        if st.session_state.extent and st.session_state.most_liked_analysis_defined:
            # Avaliação detalhada da última análise, a que o usuário mais gostou.
            logger.info(
                "Análise detalhada: {}".format(st.session_state.fr_model_order[0])
            )
            texto = st.session_state.analises[st.session_state.fr_model_order[0]]
            texto = remover_elementos_markdown(texto)
            texto = (
                texto.replace("# ", "### ").replace("## ", "### ").replace("$", r"\$")
            )
            st.markdown(texto)

            # Formulário para avaliação
            st.markdown("## Avaliação")
            with st.form("form_most_liked", clear_on_submit=True):
                caracteristicas_texto(st.session_state.fr_order)
                st.form_submit_button("Enviar", on_click=form_callback)
        else:
            # Avaliação comparativa simples
            # Definir as duas análises por ordem da lista
            logger.info("Hora da análise: {}".format(st.session_state.fr_model_order))
            texto1, texto2 = select_texts(
                st.session_state.analises, st.session_state.fr_model_order
            )

            # Preparar textos e definir as colunas
            col1, col2 = st.columns(2)

            with col1:
                st.header("Análise A")
                texto1 = remover_elementos_markdown(texto1)
                texto1 = (
                    texto1.replace("# ", "### ")
                    .replace("## ", "### ")
                    .replace("$", r"\$")
                )
                st.markdown(texto1)
            with col2:
                st.header("Análise B")
                texto2 = remover_elementos_markdown(texto2)
                texto2 = (
                    texto2.replace("# ", "### ")
                    .replace("## ", "### ")
                    .replace("$", r"\$")
                )
                st.markdown(texto2)

            # Formulário para avaliação
            st.markdown("## Avaliação")
            with st.form("form_most_liked", clear_on_submit=True):
                st.markdown("#### Qual análise você mais gostou? (Selecione uma opção)")
                st.pills(
                    "Selecione uma opção",
                    options=["Análise A", "Análise B"],
                    key="most_liked",
                    label_visibility="collapsed",
                )
                st.form_submit_button("Enviar", on_click=form_callback)


def main():
    # Configuração do Streamlit
    set_page_config()

    # Carregar dados
    load_data()

    # Execução do aplicativo
    show_interface()


if __name__ == "__main__":
    main()
