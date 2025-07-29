import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("PG_DATABASE"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT")
    )

def salvar_analise(dados: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analises_credito (
            nome_cliente,
            serasa_score,
            anotacoes_negativas,
            renda_estimada,
            capacidade_pagamento,
            comprometimento_renda,
            historico_pagamento,
            recomendacao_credito,
            limite_mensal_sugerido
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        dados["nome_cliente"],
        dados["serasa_score"],
        dados["anotacoes_negativas"],
        dados["renda_estimada"],
        dados["capacidade_pagamento"],
        dados["comprometimento_renda"],
        dados["historico_pagamento"],
        dados["recomendacao_credito"],
        dados["limite_mensal_sugerido"]
    ))

    conn.commit()
    cursor.close()
    conn.close()
