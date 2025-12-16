import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
from processor import DocumentProcessor

class DocumentProcessorGUI:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("Document Processor Pro v1.0")
        self.root.geometry("900x700")
        
        self.processor = DocumentProcessor()
        self.files_to_process = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Área de arrastar e soltar
        self.setup_drag_drop_area(main_frame)
        
        # Opções de processamento
        self.setup_options_frame(main_frame)
        
        # Botões de ação
        self.setup_action_buttons(main_frame)
        
        # Barra de progresso e logs
        self.setup_progress_logs(main_frame)
        
        # Configurar expansão
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
    def setup_drag_drop_area(self, parent):
        drop_frame = ttk.LabelFrame(parent, text="Arraste e solte arquivos aqui", padding="20")
        drop_frame.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky=(tk.W, tk.E))
        
        self.drop_label = tk.Label(
            drop_frame, 
            text="Arraste PDFs, imagens ou documentos aqui\nou clique para selecionar",
            bg="#f0f0f0",
            relief="sunken",
            height=8,
            width=80
        )
        self.drop_label.pack(fill=tk.BOTH, expand=True)
        
        # Configurar arrastar e soltar
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop)
        self.drop_label.bind('<Button-1>', self.on_click_select)
        
        # Lista de arquivos
        self.file_listbox = tk.Listbox(drop_frame, height=6, selectmode=tk.EXTENDED)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Botões para lista
        btn_frame = ttk.Frame(drop_frame)
        btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(btn_frame, text="Limpar Lista", command=self.clear_file_list).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Remover Selecionados", command=self.remove_selected_files).pack(side=tk.LEFT, padx=2)
        
    def setup_options_frame(self, parent):
        options_frame = ttk.LabelFrame(parent, text="Opções de Processamento", padding="10")
        options_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # OCR
        self.ocr_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Extrair texto com OCR", variable=self.ocr_var).grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.lang_var = tk.StringVar(value="por")
        lang_frame = ttk.Frame(options_frame)
        lang_frame.grid(row=0, column=1, sticky=tk.W, padx=20)
        ttk.Label(lang_frame, text="Idioma:").pack(side=tk.LEFT)
        ttk.Combobox(lang_frame, textvariable=self.lang_var, 
                    values=["por", "eng", "spa", "fra"], width=8).pack(side=tk.LEFT, padx=5)
        
        # Extrair tabelas
        self.tables_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Extrair tabelas para Excel", 
                       variable=self.tables_var).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Renomear arquivos
        rename_frame = ttk.Frame(options_frame)
        rename_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.rename_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(rename_frame, text="Renomear arquivos:", 
                       variable=self.rename_var).pack(side=tk.LEFT)
        
        self.rename_pattern = tk.StringVar(value="doc_{date}_{counter}")
        ttk.Entry(rename_frame, textvariable=self.rename_pattern, width=30).pack(side=tk.LEFT, padx=5)
        
        # Output format
        ttk.Label(options_frame, text="Formato de saída:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.format_var = tk.StringVar(value="xlsx")
        ttk.Combobox(options_frame, textvariable=self.format_var, 
                    values=["xlsx", "csv", "txt", "docx"], width=10).grid(row=3, column=1, sticky=tk.W)
        
    def setup_action_buttons(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=20)
        
        ttk.Button(btn_frame, text="📁 Selecionar Pasta", 
                  command=self.select_folder, width=20).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="⚙️ Processar Arquivos", 
                  command=self.process_files, width=20).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="📊 Visualizar Resultados", 
                  command=self.view_results, width=20).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="🔄 Batch Process", 
                  command=self.batch_process, width=20).pack(side=tk.LEFT, padx=5)
        
    def setup_progress_logs(self, parent):
        # Barra de progresso
        progress_frame = ttk.Frame(parent)
        progress_frame.grid(row=3, column=0, columnspan=3, pady=(10, 5), sticky=(tk.W, tk.E))
        
        ttk.Label(progress_frame, text="Progresso:").pack(side=tk.LEFT)
        self.progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.status_label = ttk.Label(progress_frame, text="Pronto")
        self.status_label.pack(side=tk.LEFT)
        
        # Área de logs
        log_frame = ttk.LabelFrame(parent, text="Log de Atividades", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = tk.Text(log_frame, height=10, width=80)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.log_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
        parent.rowconfigure(4, weight=1)
        
    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        self.add_files(files)
        
    def on_click_select(self, event):
        files = filedialog.askopenfilenames(
            title="Selecione arquivos",
            filetypes=[
                ("Documentos", "*.pdf *.jpg *.jpeg *.png *.tiff *.tif"),
                ("PDF", "*.pdf"),
                ("Imagens", "*.jpg *.jpeg *.png *.tiff *.tif"),
                ("Todos", "*.*")
            ]
        )
        if files:
            self.add_files(files)
            
    def add_files(self, files):
        for file in files:
            if file not in self.files_to_process:
                self.files_to_process.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))
        self.update_status(f"Adicionados {len(files)} arquivos")
        
    def process_files(self):
        if not self.files_to_process:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado!")
            return
            
        # Criar thread para não travar a interface
        thread = threading.Thread(target=self._process_files_thread)
        thread.daemon = True
        thread.start()
        
    def _process_files_thread(self):
        try:
            options = {
                'use_ocr': self.ocr_var.get(),
                'language': self.lang_var.get(),
                'extract_tables': self.tables_var.get(),
                'rename_files': self.rename_var.get(),
                'rename_pattern': self.rename_pattern.get(),
                'output_format': self.format_var.get()
            }
            
            self.progress['maximum'] = len(self.files_to_process)
            
            for i, file in enumerate(self.files_to_process):
                self.update_status(f"Processando: {os.path.basename(file)}")
                
                # Processar arquivo
                result = self.processor.process_document(file, options)
                
                self.log(f"✓ {os.path.basename(file)}: {result}")
                self.progress['value'] = i + 1
                self.root.update()
                
            messagebox.showinfo("Sucesso", "Processamento concluído!")
            self.progress['value'] = 0
            
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}")
            
    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
    def update_status(self, message):
        self.status_label.config(text=message)
        
    def clear_file_list(self):
        self.file_listbox.delete(0, tk.END)
        self.files_to_process.clear()
        
    def remove_selected_files(self):
        selected = self.file_listbox.curselection()
        for index in reversed(selected):
            self.file_listbox.delete(index)
            del self.files_to_process[index]
            
    def select_folder(self):
        folder = filedialog.askdirectory(title="Selecione uma pasta com documentos")
        if folder:
            import glob
            files = glob.glob(os.path.join(folder, "*.pdf")) + \
                   glob.glob(os.path.join(folder, "*.jpg")) + \
                   glob.glob(os.path.join(folder, "*.png"))
            self.add_files(files)
            
    def view_results(self):
        output_dir = self.processor.output_dir
        if os.path.exists(output_dir):
            os.startfile(output_dir)  # Abre no explorador de arquivos
            
    def batch_process(self):
        folder = filedialog.askdirectory(title="Selecione pasta para processamento em lote")
        if folder:
            self.add_files([folder])
            self.process_files()
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DocumentProcessorGUI()
    app.run()