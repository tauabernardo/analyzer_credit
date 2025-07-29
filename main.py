import json
import re
from extractor.pdf_extractor import extrair_texto_pdf
from analyzer.credit_analyzer import analisar_cliente
from db_manager import salvar_analise

def limpar_json(texto):
    """
    Extrai o primeiro JSON válido de um texto, 
    removendo blocos markdown tipo ```json ... ```
    """
    match = re.search(r"\{.*\}", texto, re.DOTALL)
    if match:
        return match.group(0)
    return "{}"  # fallback seguro

if __name__ == "__main__":
    caminho_boleto = "analyzer/data/relatoriocliente1.pdf"  # caminho correto para o seu arquivo
    
    # 1️⃣ Extrair texto do PDF
    texto = extrair_texto_pdf(caminho_boleto)
    
    # 2️⃣ Analisar com GPT
    resultado = analisar_cliente(texto)
    print("Análise de Crédito (bruto):")
    print(resultado)

    # 3️⃣ Limpar JSON e carregar em dict
    resultado_limpo = limpar_json(resultado)
    try:
        dados = json.loads(resultado_limpo)
    except json.JSONDecodeError as e:
        print("⚠ Erro ao decodificar JSON:", e)
        print("Conteúdo recebido foi:")
        print(resultado_limpo)
        exit(1)  # encerra para não salvar errado

    # 4️⃣ Salvar no PostgreSQL
    salvar_analise(dados)
    print("✅ Análise salva no PostgreSQL!")
