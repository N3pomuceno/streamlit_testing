# TODO

## Email
- [x] Modularizar email para receber os dados
- [x] Adicionar no app, seja como utils dentro do próprio arquivo
- [x] Verificar pelo Streamlit Cloud como levar a senha para lá, sem que fique exposta. [Secrets.toml](https://docs.streamlit.io/develop/api-reference/connections/secrets.toml)

## Fila de Tuplas de modelos.
- [x] Definir de forma modular a quantidade de fato relevantes, por padrão 20
- [x] Definir quantidade de análises, de forma modular que por padrão é 3. (Transitividade)
- [ ] Começar das análises de pior ranqueamento para o melhor e depois ir para a referência humana.
- [ ] Faltou algo a ser avaliado? Última pergunta. 
    - [ ] Talvez para isso criar um novo ID que facilite a identificação?
    - [ ] A cada análise humana completa, altera o índice para o próximo modelo, e a ordem da página para voltar para o início.
- [ ] Preço Humano (Mechanical Turk) x Preço LLM (Descobrir como pegar)
- [x] Manda e-mail para cada instância de análise;
- [ ] Manda e-mail para cada conjunto de análise de fato relevante realizados;
- [ ] Separar perguntas em um arquivo separado para diminuir o tamanho do arquivo principal.
- [x] Threshold para filtrar os modelos definidos;
- [x] Depois de todas as análises adicionar a análise humana para comparar.
- [ ] Página inicial para introduzir e pegar informações genéricas dos entrevistados;
- [ ] Se der, pegar informação de tempo que o usuário levou para fazer a atividade.
- [ ] Fazer análise combinatória de modelos, dos 5 estabelecidos; > Talvez isso mude para transitividade.

## Formulário
- [x] Replace de headings para pegar somente heading 3, replace de ('# ', '### ')
- [x] Criar segunda página para fazer comparação com análise humana
- [ ] Tentar de alguma forma pegar valor de tempo levado para fazer a comparação.

## Segurança
- [ ] Não expor os dados do csv que estamos utilizando. Tentando utilizar API do Google Sheets para conseguir pegar direto do google sheets.