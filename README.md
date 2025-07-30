# Analisador de Crédito - Relatórios PDF

Este projeto realiza a extração e análise de boletos em PDF utilizando OpenAI para análise de crédito, salvando os resultados em um banco de dados PostgreSQL.

---

## Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL instalado e configurado
- Conta na OpenAI e chave de API
- Git (opcional para clonar o repositório)

---

## Como configurar o ambiente
```bash
1. Clone o projeto ou copie os arquivos para seu computador:


git clone <URL-do-repositório>
cd analyzer_credit

2. Crie e ative um ambiente virtual Python:

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

3. Instale as dependências
pip install -r requirements.txt

4. Configure o banco de dados PostgreSQL:

Instale o PostgreSQL (se ainda não estiver instalado).

Crie o banco de dados e a tabela executando o script SQL ou comandos:

CREATE DATABASE analises_credito;
-- Use a base de dados e crie a tabela, exemplo:
CREATE TABLE IF NOT EXISTS analises_credito (
    id SERIAL PRIMARY KEY,
    nome_cliente TEXT,
    serasa_score TEXT,
    anotacoes_negativas TEXT,
    renda_estimada TEXT,
    capacidade_pagamento TEXT,
    comprometimento_renda TEXT,
    historico_pagamento TEXT,
    recomendacao_credito TEXT,
    limite_mensal_sugerido TEXT
);

5. Configure as variáveis de ambiente:

Crie um arquivo .env na raiz do projeto com a variável:
OPENAI_API_KEY=sua_chave_aqui
DATABASE_URL=postgresql://usuario:senha@localhost:5432/analises_credito

Como executar
Para rodar a aplicação desktop:

python app_desktop.py


Observações
Para processar PDFs, selecione os arquivos pelo botão "Selecionar PDFs" e depois clique em "Processar".

Os resultados da análise serão salvos no banco de dados automaticamente.

Se for mover o projeto para outro computador, repita os passos acima, principalmente a configuração do banco e da chave OpenAI.





