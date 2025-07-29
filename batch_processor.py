import os
import json
import re
from extractor.pdf_extractor import extrair_texto_pdf
from analyzer.credit_analyzer import analisar_cliente
from db_manager import salvar_analise

def limpar_json(texto):
    """Extrai o primeiro JSON válido do texto."""
    match = re.search(r"\{.*\}", texto, re.DOTALL)
    if match:
        return match.group(0)
    return "{}"

def processar_pdfs(pasta_pdfs):
    arquivos = [f for f in os.listdir(pasta_pdfs) if f.lower().endswith(".pdf")]
    if not arquivos:
        print("⚠ Nenhum PDF encontrado na pasta!")
        return

    for arquivo in arquivos:
        caminho = os.path.join(pasta_pdfs, arquivo)
        print(f"📄 Processando {arquivo}...")

        # Extrair texto
        texto = extrair_texto_pdf(caminho)
        # Enviar para análise GPT
        resultado = analisar_cliente(texto)
        # Limpar JSON
        resultado_limpo = limpar_json(resultado)

        try:
            dados = json.loads(resultado_limpo)
        except json.JSONDecodeError:
            print(f"⚠ Erro ao decodificar JSON para {arquivo}. Conteúdo recebido:")
            print(resultado_limpo)
            continue

        salvar_analise(dados)
        print(f"✅ Análise salva para {arquivo}!\n")

if __name__ == "__main__":
    pasta = "analyzer/data/pdfs"  # coloque aqui seus PDFs
    processar_pdfs(pasta)
