# TODO

## Email
- [x] Modularizar email para receber os dados
- [x] Adicionar no app, seja como utils dentro do próprio arquivo
- [x] Verificar pelo Streamlit Cloud como levar a senha para lá, sem que fique exposta. [Secrets.toml](https://docs.streamlit.io/develop/api-reference/connections/secrets.toml)

## Fila de Tuplas de modelos.
- [ ] Fazer análise combinatória de modelos, dos 5 estabelecidos;
- [ ] Threshold para filtrar os modelos definidos;
- [ ] Depois de todas as análises adicionar a análise humana para comparar.
- [ ] Página inicial para introduzir e pegar informações genéricas dos entrevistados;
- [ ] Se der, pegar informação de tempo que o usuário levou para fazer a atividade.

## Formulário
- [x] Replace de headings para pegar somente heading 3, replace de ('# ', '### ')
- [ ] Criar segunda página para fazer comparação com análise humana
- [ ] Tentar de alguma forma pegar valor de tempo levado para fazer a comparação.

## Segurança
- [ ] Não expor os dados do csv que estamos utilizando. Tentando utilizar API do Google Sheets para conseguir pegar direto do google sheets.