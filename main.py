import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import threading
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
from processor import DocumentProcessor
from datetime import datetime

class DocumentProcessorGUI:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("📄 Document Processor Pro v2.0")
        self.root.geometry("1100x800")
        self.root.configure(bg="#2b2b2b")
        
        # Configurar ícone (opcional)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        self.processor = DocumentProcessor()
        self.files_to_process = []
        
        # Configurar estilo moderno
        self.setup_styles()
        self.setup_ui()
        
        # Centralizar janela
        self.center_window()
        
    def setup_styles(self):
        """Configura estilos modernos"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cores modernas
        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.accent_color = "#3498db"
        self.success_color = "#2ecc71"
        self.warning_color = "#e74c3c"
        self.card_bg = "#34495e"
        self.hover_color = "#2980b9"
        self.process_color = "#9b59b6"  # Nova cor para botão de processar
        
        # Configurar estilos
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10)
        self.style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        self.style.configure("Card.TFrame", background=self.card_bg, relief="flat", borderwidth=0)
        
        # Botões personalizados
        self.style.configure("Process.TButton", 
                           background=self.process_color,
                           foreground="white",
                           borderwidth=0,
                           focuscolor="none",
                           font=("Segoe UI", 12, "bold"))
        self.style.map("Process.TButton",
                      background=[("active", "#8e44ad")])
        
        self.style.configure("Accent.TButton", 
                           background=self.accent_color,
                           foreground="white",
                           borderwidth=0,
                           focuscolor="none")
        self.style.map("Accent.TButton",
                      background=[("active", self.hover_color)])
        
        self.style.configure("Success.TButton",
                           background=self.success_color,
                           foreground="white")
        
        self.style.configure("Warning.TButton",
                           background=self.warning_color,
                           foreground="white")
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_height() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Configura a interface moderna"""
        # Container principal com padding
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        self.setup_header(main_container)
        
        # Área principal com duas colunas
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Coluna esquerda (Upload e arquivos)
        left_frame = ttk.Frame(content_frame, width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Coluna direita (Configurações e logs)
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Configurar conteúdo
        self.setup_file_upload(left_frame)
        self.setup_file_list(left_frame)
        self.setup_options(right_frame)
        self.setup_progress_logs(right_frame)
        
        # BOTÃO DE PROCESSAR PRINCIPAL (agora mais destacado)
        self.setup_process_button(main_container)
        
        # Botões de ação adicionais
        self.setup_action_buttons(main_container)
        
        # Rodapé
        self.setup_footer(main_container)
    
    def setup_header(self, parent):
        """Configura cabeçalho moderno"""
        header_frame = ttk.Frame(parent, style="Card.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo e título
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=15)
        
        ttk.Label(title_frame, text="📄", font=("Segoe UI", 32)).pack(side=tk.LEFT)
        
        title_text = ttk.Label(title_frame, 
                              text="Document Processor Pro",
                              style="Title.TLabel")
        title_text.pack(side=tk.LEFT, padx=(10, 0))
        
        subtitle = ttk.Label(title_frame,
                           text="Transforme documentos em dados estruturados",
                           font=("Segoe UI", 9),
                           foreground="#95a5a6")
        subtitle.pack(side=tk.LEFT, padx=(15, 0))
        
        # Estatísticas
        stats_frame = ttk.Frame(header_frame, style="Card.TFrame")
        stats_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.stats_label = ttk.Label(stats_frame,
                                    text="📊 0 arquivos | 0 processados",
                                    font=("Segoe UI", 9),
                                    foreground="#ecf0f1")
        self.stats_label.pack()
    
    def setup_file_upload(self, parent):
        """Configura área de upload moderna"""
        upload_card = ttk.Frame(parent, style="Card.TFrame")
        upload_card.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(upload_card, 
                 text="📤 Upload de Arquivos",
                 font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        # Área de drag & drop moderna
        self.drop_frame = tk.Frame(upload_card, 
                                  bg="#3b4b5c", 
                                  relief="flat",
                                  bd=2,
                                  highlightbackground=self.accent_color,
                                  highlightthickness=2,
                                  highlightcolor=self.accent_color)
        self.drop_frame.pack(fill=tk.BOTH, padx=20, pady=(0, 15), expand=True)
        
        self.drop_label = tk.Label(self.drop_frame,
                                  text="⬆️ ARRASTE E SOLTE AQUI\nou clique para selecionar arquivos",
                                  bg="#3b4b5c",
                                  fg="#ecf0f1",
                                  font=("Segoe UI", 11),
                                  relief="flat",
                                  height=8)
        self.drop_label.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Configurar drag & drop
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop)
        self.drop_label.bind('<Button-1>', self.on_click_select)
        self.drop_label.bind('<Enter>', lambda e: self.drop_frame.config(bg="#4a5a6b"))
        self.drop_label.bind('<Leave>', lambda e: self.drop_frame.config(bg="#3b4b5c"))
        
        # Botões de ação rápidos
        btn_frame = ttk.Frame(upload_card)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        ttk.Button(btn_frame, 
                  text="📁 Selecionar Arquivos",
                  command=self.on_click_select,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(btn_frame,
                  text="📂 Selecionar Pasta",
                  command=self.select_folder).pack(side=tk.LEFT)
    
    def setup_file_list(self, parent):
        """Configura lista de arquivos moderna"""
        list_card = ttk.Frame(parent, style="Card.TFrame")
        list_card.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(list_card,
                 text="📋 Arquivos para Processar",
                 font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        # Container com scroll
        list_container = ttk.Frame(list_card)
        list_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox personalizado
        self.file_listbox = tk.Listbox(list_container,
                                      bg="#3b4b5c",
                                      fg="#ecf0f1",
                                      selectbackground=self.accent_color,
                                      selectforeground="white",
                                      font=("Segoe UI", 10),
                                      relief="flat",
                                      borderwidth=0,
                                      highlightthickness=0,
                                      yscrollcommand=scrollbar.set)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.file_listbox.yview)
        
        # Botões da lista
        btn_frame = ttk.Frame(list_card)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        ttk.Button(btn_frame,
                  text="🗑️ Limpar Lista",
                  command=self.clear_file_list,
                  style="Warning.TButton").pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(btn_frame,
                  text="✂️ Remover Selecionados",
                  command=self.remove_selected_files).pack(side=tk.LEFT)
    
    def setup_options(self, parent):
        """Configura opções de processamento"""
        options_card = ttk.Frame(parent, style="Card.TFrame")
        options_card.pack(fill=tk.BOTH, pady=(0, 15))
        
        ttk.Label(options_card,
                 text="⚙️ Configurações de Processamento",
                 font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        # Grid para opções
        options_grid = ttk.Frame(options_card)
        options_grid.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Linha 1: OCR
        self.ocr_var = tk.BooleanVar(value=True)
        ocr_check = ttk.Checkbutton(options_grid,
                                   text="🔤 Extrair texto com OCR",
                                   variable=self.ocr_var,
                                   style="TLabel")
        ocr_check.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.lang_var = tk.StringVar(value="por")
        lang_combo = ttk.Combobox(options_grid,
                                 textvariable=self.lang_var,
                                 values=["por", "eng", "spa", "fra"],
                                 state="readonly",
                                 width=10)
        lang_combo.grid(row=0, column=1, sticky=tk.W, padx=20, pady=5)
        
        # Linha 2: Tabelas
        self.tables_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_grid,
                       text="📊 Extrair tabelas para Excel",
                       variable=self.tables_var,
                       style="TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Linha 3: Renomear
        rename_frame = ttk.Frame(options_grid)
        rename_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.rename_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(rename_frame,
                       text="✏️ Renomear arquivos:",
                       variable=self.rename_var,
                       style="TLabel").pack(side=tk.LEFT)
        
        self.rename_pattern = tk.StringVar(value="doc_{date}_{counter:03d}")
        rename_entry = ttk.Entry(rename_frame,
                                textvariable=self.rename_pattern,
                                width=30)
        rename_entry.pack(side=tk.LEFT, padx=5)
        
        # Linha 4: Formato
        ttk.Label(options_grid,
                 text="📁 Formato de saída:").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.format_var = tk.StringVar(value="xlsx")
        format_combo = ttk.Combobox(options_grid,
                                   textvariable=self.format_var,
                                   values=["xlsx", "csv", "txt", "docx"],
                                   state="readonly",
                                   width=10)
        format_combo.grid(row=3, column=1, sticky=tk.W, padx=20, pady=5)
    
    def setup_progress_logs(self, parent):
        """Configura progresso e logs"""
        logs_card = ttk.Frame(parent, style="Card.TFrame")
        logs_card.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(logs_card,
                 text="📈 Progresso e Logs",
                 font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        # Barra de progresso
        progress_frame = ttk.Frame(logs_card)
        progress_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        ttk.Label(progress_frame,
                 text="Progresso:",
                 font=("Segoe UI", 10)).pack(side=tk.LEFT)
        
        self.progress = ttk.Progressbar(progress_frame,
                                       length=300,
                                       mode='determinate',
                                       style="TProgressbar")
        self.progress.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.progress_percent = ttk.Label(progress_frame,
                                         text="0%",
                                         font=("Segoe UI", 10, "bold"),
                                         foreground=self.accent_color)
        self.progress_percent.pack(side=tk.LEFT)
        
        # Área de logs com scroll
        logs_frame = ttk.Frame(logs_card)
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Text widget com scroll
        text_frame = ttk.Frame(logs_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(text_frame,
                               bg="#3b4b5c",
                               fg="#ecf0f1",
                               insertbackground="white",
                               selectbackground=self.accent_color,
                               font=("Consolas", 9),
                               relief="flat",
                               borderwidth=0,
                               wrap=tk.WORD,
                               height=8)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar personalizada
        log_scroll = ttk.Scrollbar(text_frame,
                                  command=self.log_text.yview)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=log_scroll.set)
        
        # Tags para colorir logs
        self.log_text.tag_config("SUCCESS", foreground=self.success_color)
        self.log_text.tag_config("ERROR", foreground=self.warning_color)
        self.log_text.tag_config("INFO", foreground=self.accent_color)
        self.log_text.tag_config("WARNING", foreground="#f39c12")
    
    def setup_process_button(self, parent):
        """Configura o botão principal de processamento (AGORA MAIS DESTACADO)"""
        process_frame = ttk.Frame(parent)
        process_frame.pack(fill=tk.X, pady=(20, 10))
        
        # Botão GRANDE e destacado
        self.process_btn = ttk.Button(process_frame,
                                     text="🚀 PROCESSAR ARQUIVOS",
                                     command=self.process_files,
                                     style="Process.TButton",
                                     width=30)
        self.process_btn.pack(pady=10)
        
        # Label de instrução
        ttk.Label(process_frame,
                 text="Clique aqui para iniciar o processamento dos arquivos selecionados",
                 font=("Segoe UI", 9),
                 foreground="#95a5a6").pack()
    
    def setup_action_buttons(self, parent):
        """Configura botões de ação adicionais"""
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Botões em uma linha
        buttons = [
            ("📂 Abrir Resultados", self.view_results, "Accent.TButton"),
            ("🔄 Processar Pasta", self.batch_process, "Accent.TButton"),
            ("⚙️ Configurações", self.show_settings, "Accent.TButton"),
            ("❓ Ajuda", self.show_help, "Accent.TButton")
        ]
        
        for text, command, style in buttons:
            btn = ttk.Button(action_frame,
                           text=text,
                           command=command,
                           style=style)
            btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def setup_footer(self, parent):
        """Configura rodapé"""
        footer_frame = ttk.Frame(parent, style="Card.TFrame")
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Informações do sistema
        info_frame = ttk.Frame(footer_frame)
        info_frame.pack(padx=20, pady=10)
        
        # Status do sistema
        self.system_status = ttk.Label(info_frame,
                                      text="✅ Sistema pronto",
                                      font=("Segoe UI", 9),
                                      foreground=self.success_color)
        self.system_status.pack(side=tk.LEFT)
        
        # Separador
        ttk.Label(info_frame, text="|").pack(side=tk.LEFT, padx=10)
        
        # Memória e recursos
        self.resource_label = ttk.Label(info_frame,
                                       text="💾 RAM: -- | CPU: --%",
                                       font=("Segoe UI", 9),
                                       foreground="#95a5a6")
        self.resource_label.pack(side=tk.LEFT)
        
        # Separador
        ttk.Label(info_frame, text="|").pack(side=tk.LEFT, padx=10)
        
        # Versão
        ttk.Label(info_frame,
                 text=f"Versão 2.0 • {datetime.now().year}",
                 font=("Segoe UI", 9),
                 foreground="#95a5a6").pack(side=tk.LEFT)
        
        # Atualizar recursos periodicamente
        self.update_resources()
    
    def update_resources(self):
        """Atualiza informações de recursos do sistema"""
        try:
            import psutil
            ram = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=0.1)
            self.resource_label.config(text=f"💾 RAM: {ram.percent}% | CPU: {cpu}%")
        except:
            self.resource_label.config(text="💾 Monitoramento não disponível")
        
        # Agendar próxima atualização
        self.root.after(2000, self.update_resources)
    
    def show_help(self):
        """Mostra janela de ajuda"""
        help_text = """
        📚 AJUDA - Document Processor Pro
        
        COMO USAR:
        1. Arraste arquivos para a área colorida
        2. Ou clique em 'Selecionar Arquivos'
        3. Configure as opções de processamento
        4. Clique no botão grande '🚀 PROCESSAR ARQUIVOS'
        5. Acesse os resultados na pasta 'data/output/'
        
        DICAS:
        • Use Ctrl+Click para selecionar múltiplos arquivos na lista
        • Para extrair texto de imagens, marque 'Extrair texto com OCR'
        • Para tabelas, marque 'Extrair tabelas para Excel'
        
        SUPORTE:
        • Verifique se o Tesseract OCR está instalado
        • Os arquivos de idioma devem estar em tessdata/
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Ajuda - Document Processor")
        help_window.geometry("500x400")
        help_window.configure(bg=self.bg_color)
        
        # Centralizar
        help_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (500 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (400 // 2)
        help_window.geometry(f"500x400+{x}+{y}")
        
        # Texto de ajuda
        text_widget = tk.Text(help_window,
                             bg="#3b4b5c",
                             fg="#ecf0f1",
                             font=("Segoe UI", 10),
                             wrap=tk.WORD,
                             padx=20,
                             pady=20)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")
        
        # Botão de fechar
        ttk.Button(help_window,
                  text="Fechar",
                  command=help_window.destroy,
                  style="Accent.TButton").pack(pady=10)
    
    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        self.add_files(files)
    
    def on_click_select(self, event=None):
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
                self.file_listbox.insert(tk.END, f"📄 {os.path.basename(file)}")
        
        self.update_stats()
        self.log("📁 Arquivos adicionados", "INFO")
        
        # Ativar botão de processar se houver arquivos
        self.process_btn.config(state="normal" if self.files_to_process else "disabled")
    
    def update_stats(self):
        """Atualiza estatísticas na interface"""
        count = len(self.files_to_process)
        self.stats_label.config(text=f"📊 {count} arquivo(s) | 0 processado(s)")
    
    def process_files(self):
        if not self.files_to_process:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado para processamento!")
            return
        
        self.log("🚀 Iniciando processamento...", "INFO")
        self.process_btn.config(state="disabled", text="⏳ Processando...")
        
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
            
            total = len(self.files_to_process)
            self.progress['maximum'] = total
            
            for i, file in enumerate(self.files_to_process):
                filename = os.path.basename(file)
                self.log(f"⏳ Processando: {filename} ({i+1}/{total})", "INFO")
                self.system_status.config(text=f"⏳ Processando {filename}")
                
                try:
                    result = self.processor.process_document(file, options)
                    self.log(f"✅ {filename}: {result}", "SUCCESS")
                except Exception as e:
                    self.log(f"❌ {filename}: {str(e)}", "ERROR")
                
                # Atualizar progresso
                progress_value = i + 1
                self.progress['value'] = progress_value
                percent = int((progress_value / total) * 100)
                self.progress_percent.config(text=f"{percent}%")
                self.root.update()
            
            self.log("🎉 Processamento concluído com sucesso!", "SUCCESS")
            self.system_status.config(text="✅ Sistema pronto")
            self.progress['value'] = 0
            self.progress_percent.config(text="0%")
            
            messagebox.showinfo("Sucesso", f"Processamento concluído!\n{total} arquivo(s) processado(s).")
            
        except Exception as e:
            self.log(f"💥 Erro crítico: {str(e)}", "ERROR")
            messagebox.showerror("Erro", f"Ocorreu um erro durante o processamento:\n{str(e)}")
        
        finally:
            # Reativar botão
            self.process_btn.config(state="normal", text="🚀 PROCESSAR ARQUIVOS")
    
    def log(self, message, level="INFO"):
        """Adiciona mensagem ao log com formatação"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, formatted, level)
        self.log_text.see(tk.END)
    
    def clear_file_list(self):
        if self.files_to_process:
            self.file_listbox.delete(0, tk.END)
            self.files_to_process.clear()
            self.update_stats()
            self.log("🗑️ Lista de arquivos limpa", "INFO")
            self.process_btn.config(state="disabled")
    
    def remove_selected_files(self):
        selected = self.file_listbox.curselection()
        if selected:
            for index in reversed(selected):
                self.file_listbox.delete(index)
                del self.files_to_process[index]
            self.update_stats()
            self.log(f"✂️ {len(selected)} arquivo(s) removido(s)", "INFO")
            
            # Atualizar estado do botão
            self.process_btn.config(state="normal" if self.files_to_process else "disabled")
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="Selecione uma pasta com documentos")
        if folder:
            import glob
            files = []
            for ext in ['*.pdf', '*.jpg', '*.jpeg', '*.png', '*.tiff', '*.tif']:
                files.extend(glob.glob(os.path.join(folder, ext)))
            
            if files:
                self.add_files(files)
                self.log(f"📂 Pasta '{os.path.basename(folder)}' carregada", "INFO")
    
    def view_results(self):
        output_dir = self.processor.output_dir
        if os.path.exists(output_dir):
            os.startfile(output_dir)
            self.log("📂 Pasta de resultados aberta", "INFO")
    
    def batch_process(self):
        folder = filedialog.askdirectory(title="Selecione pasta para processamento em lote")
        if folder:
            self.add_files([folder])
            self.process_files()
    
    def show_settings(self):
        """Mostra diálogo de configurações avançadas"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Configurações Avançadas")
        settings_window.geometry("500x400")
        settings_window.configure(bg=self.bg_color)
        
        # Centralizar
        settings_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (500 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (400 // 2)
        settings_window.geometry(f"500x400+{x}+{y}")
        
        ttk.Label(settings_window,
                 text="Configurações Avançadas",
                 font=("Segoe UI", 14, "bold")).pack(pady=20)
        
        # Adicione mais configurações aqui conforme necessário
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DocumentProcessorGUI()
    app.run()