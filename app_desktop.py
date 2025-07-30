import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import json
import re
from extractor.pdf_extractor import extrair_texto_pdf
from analyzer.credit_analyzer import analisar_cliente
from db_manager import salvar_analise

def limpar_json(texto):
    """Extrai o primeiro JSON válido do texto retornado pelo GPT."""
    match = re.search(r"\{.*\}", texto, re.DOTALL)
    return match.group(0) if match else "{}"

def extrair_score(texto):
    """
    Extrai o Serasa Score do texto do PDF.
    O score sempre vem antes da porcentagem de chance de pagamento.
    Exemplo: "1000 96,30% de chance de pagamento"
    """
    match = re.search(r'(\d{3,4})\s+\d{1,3},\d{2}%\s+de chance de pagamento', texto, re.IGNORECASE)
    if match:
        return match.group(1)
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
        texto = extrair_texto_pdf(arquivo)
        resultado = analisar_cliente(texto)
        resultado_limpo = limpar_json(resultado)

        try:
            dados = json.loads(resultado_limpo)

            # Corrigir score via regex se encontrado
            score_regex = extrair_score(texto)
            if score_regex:
                dados["serasa_score"] = score_regex

            salvar_analise(dados)
            log_text.insert(
                tk.END, 
                f"✅ Salvo no banco: {dados.get('nome_cliente', 'Sem nome')} - Score: {dados.get('serasa_score', 'N/A')}\n\n"
            )

        except json.JSONDecodeError:
            log_text.insert(tk.END, f"❌ Erro ao decodificar JSON para {arquivo}\n\n")

    messagebox.showinfo("Concluído", "Todos os arquivos foram processados!")

# ---- Interface Tkinter ----
janela = tk.Tk()
janela.title("Analisador de Crédito - Desktop")
janela.geometry("600x400")

lista_arquivos = []

frame = tk.Frame(janela)
frame.pack(pady=10)

btn_selecionar = tk.Button(frame, text="📂 Selecionar PDFs", command=selecionar_arquivos)
btn_selecionar.grid(row=0, column=0, padx=5)

btn_processar = tk.Button(frame, text="⚡ Processar", command=processar_arquivos)
btn_processar.grid(row=0, column=1, padx=5)

log_text = scrolledtext.ScrolledText(janela, wrap=tk.WORD, width=70, height=20)
log_text.pack(padx=10, pady=10)

janela.mainloop()
