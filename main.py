from extractor.pdf_extractor import extrair_texto_pdf
from analyzer.credit_analyzer import analisar_cliente

if __name__ == "__main__":
    caminho_boleto = "analyzer/data/relatoriocliente1.pdf"  # caminho correto para o seu arquivo
    texto = extrair_texto_pdf(caminho_boleto)
    
    print("Texto processado e limpo do boleto:")
    print(texto)

    resultado = analisar_cliente(texto)
    print("Análise de Crédito:")
    print(resultado)
