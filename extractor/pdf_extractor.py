import PyPDF2
import re

def extrair_texto_pdf(caminho_pdf):
    with open(caminho_pdf, "rb") as arquivo:
        reader = PyPDF2.PdfReader(arquivo)
        texto = ""
        for pagina in reader.pages:
            texto += pagina.extract_text()

    # Limpar dados sensíveis
    padroes = [
        r"\d{3}\.\d{3}\.\d{3}-\d{2}",   # CPF formatado
        r"\b\d{11}\b",                  # CPF só números
        r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}",  # CNPJ
        r"55\d{11}"                     # Telefone internacional
    ]

    for padrao in padroes:
        texto = re.sub(padrao, "[DADO_REDACTED]", texto)

    return texto
