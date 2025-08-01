import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import json
import re
import fitz  # PyMuPDF
from extractor.pdf_extractor import extrair_texto_pdf
from analyzer.credit_analyzer import analisar_cliente
from db_manager import salvar_analise

# -------------------------------------------------------
# Funções auxiliares
# -------------------------------------------------------

def limpar_json(texto):
    """Extrai o primeiro JSON válido do texto retornado pelo GPT."""
    match = re.search(r"\{.*\}", texto, re.DOTALL)
    return match.group(0) if match else "{}"

def extrair_score_pymupdf(caminho_pdf):
    """
    Extrai o Serasa Score com PyMuPDF pegando o número grande próximo à frase de chance de pagamento.
    """
    try:
        doc = fitz.open(caminho_pdf)
        primeira_pagina = doc[0]
        texto = primeira_pagina.get_text("text")

        # Regex para localizar padrão "1000 96,30% de chance de pagamento"
        match = re.search(r'(\d{3,4})\s+\d{1,3}[.,]\d{2}%\s+de chance de pagamento', texto, re.IGNORECASE)
        if match:
            return match.group(1)

        # Se não achar, tenta pegar o maior número da página (normalmente é o score)
        numeros = re.findall(r'\b\d{3,4}\b', texto)
        if numeros:
            return max(numeros, key=int)

        return None
    except Exception:
        return None

def selecionar_arquivos():
    arquivos = filedialog.askopenfilenames(
        title="Selecione os boletos em PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if arquivos:
        lista_arquivos.extend(arquivos)
        messagebox.showinfo("Arquivos adicionados", f"{len(arquivos)} arquivo(s) adicionado(s).")

def processar_arquivos():
    if not lista_arquivos:
        messagebox.showwarning("Aviso", "Nenhum arquivo selecionado!")
        return
    
    for arquivo in lista_arquivos:
        log_text.insert(tk.END, f"📄 Processando {os.path.basename(arquivo)}...\n")
        log_text.see(tk.END)

        # Extrai texto completo para análise
        texto = extrair_texto_pdf(arquivo)

        # Extrai score com PyMuPDF
        score_exato = extrair_score_pymupdf(arquivo)

        # Chama análise do GPT
        resultado = analisar_cliente(texto)
        resultado_limpo = limpar_json(resultado)

        try:
            dados = json.loads(resultado_limpo)
            dados["serasa_score"] = score_exato or dados.get("serasa_score", "N/A")

            salvar_analise(dados)
            log_text.insert(
                tk.END, 
                f"✅ Salvo no banco: {dados.get('nome_cliente', 'Sem nome')} - Score: {dados['serasa_score']}\n\n"
            )
        except json.JSONDecodeError:
            log_text.insert(tk.END, f"❌ Erro ao decodificar JSON para {arquivo}\n\n")

        log_text.see(tk.END)

    messagebox.showinfo("Concluído", "Todos os arquivos foram processados!")
    lista_arquivos.clear()

# -------------------------------------------------------
# Interface Tkinter
# -------------------------------------------------------
janela = tk.Tk()
janela.title("Analisador de Crédito - Desktop")
janela.geometry("850x550")

lista_arquivos = []

frame = tk.Frame(janela)
frame.pack(pady=10)

btn_selecionar = tk.Button(frame, text="📂 Selecionar PDFs", width=20, command=selecionar_arquivos)
btn_selecionar.grid(row=0, column=0, padx=5)

btn_processar = tk.Button(frame, text="⚡ Processar", width=20, command=processar_arquivos)
btn_processar.grid(row=0, column=1, padx=5)

log_text = scrolledtext.ScrolledText(janela, wrap=tk.WORD, width=100, height=25)
log_text.pack(padx=10, pady=10)

janela.mainloop()
