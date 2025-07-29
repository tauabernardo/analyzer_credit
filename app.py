import streamlit as st
import os
import json
import re
from extractor.pdf_extractor import extrair_texto_pdf
from analyzer.credit_analyzer import analisar_cliente
from db_manager import salvar_analise

# Pasta onde os PDFs serão salvos
PASTA_PDFS = "analyzer/data/pdfs"
os.makedirs(PASTA_PDFS, exist_ok=True)

def limpar_json(texto):
    match = re.search(r"\{.*\}", texto, re.DOTALL)
    if match:
        return match.group(0)
    return "{}"

st.title("📄 Analisador de Crédito - Boletos PDF")

# Upload de arquivos
uploaded_files = st.file_uploader("Envie boletos em PDF", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Salvar arquivo na pasta
        caminho_pdf = os.path.join(PASTA_PDFS, uploaded_file.name)
        with open(caminho_pdf, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.write(f"📥 Arquivo salvo: {uploaded_file.name}")

        # Extrair e analisar
        texto = extrair_texto_pdf(caminho_pdf)
        resultado = analisar_cliente(texto)
        resultado_limpo = limpar_json(resultado)

        try:
            dados = json.loads(resultado_limpo)
            salvar_analise(dados)
            st.success(f"✅ Análise concluída e salva no banco para {uploaded_file.name}!")
            st.json(dados)
        except json.JSONDecodeError:
            st.error(f"❌ Erro ao decodificar JSON para {uploaded_file.name}")
            st.text(resultado)
