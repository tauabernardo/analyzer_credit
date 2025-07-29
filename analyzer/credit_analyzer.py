import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analisar_cliente(texto_pdf):
    prompt = f"""
Você é um analista de crédito.  
A partir das informações do boleto a seguir, avalie:

1. Serasa Score
2. Anotações Negativas
3. Renda Estimada
4. Capacidade de pagamento
5. Comprometimento de renda
6. Histórico de Pagamento
7. Recomenda conceder crédito? (Sim/Não)
8. Limite mensal sugerido

Boleto:
{texto_pdf}

Responda em JSON estruturado assim:
{{
  "serasa_score": "",
  "anotacoes_negativas": "",
  "renda_estimada": "",
  "capacidade_pagamento": "",
  "comprometimento_renda": "",
  "historico_pagamento": "",
  "recomendacao_credito": "",
  "limite_mensal_sugerido": ""
}}
    """

    response = client.responses.create(
        model="gpt-4.1-mini", 
        input=prompt
    )

    return response.output_text
