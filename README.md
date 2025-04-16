# crowd-evaluate

Repositório dedicado para subir uma aplicação Streamlit, que faça o papel de formulário para os usuários que irão ajudar verificar se dados gerados pelos modelos de linguagem são válidos ou não.

Atualmente para executar a aplicação, estou utilizando o uv.

Para rodar a aplicação, basta entrar no ambiente virtual gerado pelo uv e depois dar um run no projeto para ver localmente. Caso queira ver no Streamlit Cloud, siga os passos no seguinte [link](https://streamlit.io/cloud)


Localmente:
```bash
# Instalar pacotes necessários
uv sync

# Abrir a venv
source .venv/bin/activate

#Rodar aplicação 
streamlit run app.py
```


Formato padrão de Execução:

```mermaid
flowchart TD
A[Entrada]-->|Definição de Granularidade|E[Fatos Relevantes e suas análises]
E-->B[Especialização das análises]
E-->|Caso não queria o grão mais fino|C[Definição que de qual modelo mais gosta]
C-->B
B-->|Retorna para o próximo Documento|E
```