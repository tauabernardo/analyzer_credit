import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analisar_cliente(texto_pdf):
    prompt = f"""
Você é um analista de crédito.  
Extraia do texto do boleto abaixo:

{texto_pdf}

- Nome completo do cliente
- Serasa Score (ex: 350, valor que fica no inicio do texto próximo a Serasa Score)
- Anotações negativas **bem resumidas** (apenas quantidade + tipo, ex: "6 financeiras, 6 protestos")
- Renda estimada mensal (ex: "R$ 5000", tem que ser o valor de renda estimada e não renda mais)
- Capacidade de pagamento mensal (valor numérico ou em reais)
- Comprometimento de renda percentual (ex: "25%")
- Histórico de pagamento resumido (ex: "Bom", "Regular", "Ruim")
- Recomenda concessão de crédito? (Sim/Não)
- Limite mensal sugerido em reais (apenas valor ou "0" se não recomendado)

Responda em JSON estruturado assim:

{{
  "nome_cliente": "",
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
