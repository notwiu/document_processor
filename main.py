import customtkinter as ctk
from tkinter import filedialog, messagebox
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import camelot
import pandas as pd
import os
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

LICENCA_VALIDA = "PRO-2025"

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("DocFlow Pro")
        self.geometry("1100x700")
        self.resizable(False, False)

        self.arquivos = []
        self.pasta_saida = ""

        self.login_screen()

    # ---------------- LOGIN ----------------
    def login_screen(self):
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(expand=True)

        ctk.CTkLabel(
            self.login_frame,
            text="DocFlow Pro",
            font=("Segoe UI", 32, "bold")
        ).pack(pady=20)

        self.licenca_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Digite sua licença",
            width=300
        )
        self.licenca_entry.pack(pady=10)

        ctk.CTkButton(
            self.login_frame,
            text="Ativar",
            command=self.validar_licenca,
            width=200
        ).pack(pady=20)

    def validar_licenca(self):
        if self.licenca_entry.get() == LICENCA_VALIDA:
            self.login_frame.destroy()
            self.main_screen()
        else:
            messagebox.showerror("Erro", "Licença inválida")

    # ---------------- MAIN UI ----------------
    def main_screen(self):

        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.sidebar,
            text="Menu",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)

        ctk.CTkButton(
            self.sidebar,
            text="Selecionar PDFs",
            command=self.selecionar_pdfs
        ).pack(pady=10, padx=10)

        ctk.CTkButton(
            self.sidebar,
            text="Processar",
            command=self.processar
        ).pack(pady=10, padx=10)

        # Conteúdo
        self.content = ctk.CTkFrame(self)
        self.content.pack(expand=True, fill="both", padx=10, pady=10)

        # Status
        self.status_label = ctk.CTkLabel(
            self.content,
            text="Nenhum arquivo selecionado",
            font=("Segoe UI", 14)
        )
        self.status_label.pack(anchor="w", pady=5)

        # Opções
        options = ctk.CTkFrame(self.content)
        options.pack(fill="x", pady=10)

        self.ocr_var = ctk.BooleanVar(value=True)
        self.excel_var = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(
            options,
            text="Extrair Texto (TXT)",
            variable=self.ocr_var
        ).pack(side="left", padx=20)

        ctk.CTkCheckBox(
            options,
            text="Extrair Tabelas (Excel)",
            variable=self.excel_var
        ).pack(side="left", padx=20)

        # Preview
        ctk.CTkLabel(
            self.content,
            text="Preview OCR",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", pady=5)

        self.preview_box = ctk.CTkTextbox(self.content, height=250)
        self.preview_box.pack(fill="x", pady=5)

        self.progress = ctk.CTkProgressBar(self.content)
        self.progress.pack(fill="x", pady=10)
        self.progress.set(0)

    # ---------------- FUNCIONALIDADES ----------------
    def selecionar_pdfs(self):
        self.arquivos = filedialog.askopenfilenames(
            filetypes=[("PDF", "*.pdf")]
        )
        self.status_label.configure(
            text=f"{len(self.arquivos)} arquivos selecionados"
        )

    def processar(self):
        if not self.arquivos:
            messagebox.showwarning("Aviso", "Selecione PDFs")
            return

        self.pasta_saida = filedialog.askdirectory()
        if not self.pasta_saida:
            return

        threading.Thread(target=self.executar).start()

    def executar(self):
        self.progress.set(0)
        total = len(self.arquivos)

        for i, pdf in enumerate(self.arquivos):
            nome = os.path.splitext(os.path.basename(pdf))[0]

            # OCR
            if self.ocr_var.get():
                imagens = convert_from_path(pdf)
                texto = ""
                for img in imagens:
                    texto += pytesseract.image_to_string(img, lang="por")

                with open(
                    os.path.join(self.pasta_saida, f"{nome}.txt"),
                    "w",
                    encoding="utf-8"
                ) as f:
                    f.write(texto)

                self.preview_box.delete("1.0", "end")
                self.preview_box.insert("1.0", texto[:1000])

            # Excel
            if self.excel_var.get():
                try:
                    tabelas = camelot.read_pdf(pdf, pages="1")
                    for idx, tabela in enumerate(tabelas):
                        tabela.df.to_excel(
                            os.path.join(
                                self.pasta_saida,
                                f"{nome}_tabela_{idx+1}.xlsx"
                            ),
                            index=False
                        )
                except:
                    pass

            self.progress.set((i + 1) / total)

        self.status_label.configure(text="Processamento concluído")
        messagebox.showinfo("Sucesso", "Arquivos processados com sucesso")

if __name__ == "__main__":
    App().mainloop()