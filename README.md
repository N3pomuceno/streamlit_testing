# crowd-evaluate

Repositório dedicado para subir uma aplicação Streamlit, que faça o papel de formulário para os usuários que irão ajudar verificar se dados gerados pelos modelos de linguagem são válidos ou não.

Atualmente para executar a aplicação, estou utilizando uma versão do gerenciador de pacotes antigo, que é o poetry 1.8.3, porém depois atualizarei para ficar em dia com versão mais moderna.

Para rodar a aplicação, basta entrar no ambiente virtual gerado pelo poetry e depois dar um run no projeto para ver localmente. Caso queira ver no Streamlit Cloud, siga os passos no seguinte [link](https://streamlit.io/cloud)


Localmente:
```bash
# Abrir a venv
poetry shell

# Instalar dependências
poetry install

#Rodar aplicação 
streamlit run app.py
```