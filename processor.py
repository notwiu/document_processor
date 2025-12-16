import os
import shutil
from datetime import datetime
from pathlib import Path
import pytesseract
from pdf2image import convert_from_path
import pdfplumber
import pandas as pd
from PIL import Image
import openpyxl
from ocr_handler import OCRHandler
from pdf_handler import PDFHandler
from excel_handler import ExcelHandler
from file_organizer import FileOrganizer

class DocumentProcessor:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(self.base_dir, "data", "output")
        self.temp_dir = os.path.join(self.base_dir, "temp")
        
        # Criar diretórios se não existirem
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Inicializar handlers
        self.ocr = OCRHandler()
        self.pdf = PDFHandler()
        self.excel = ExcelHandler()
        self.organizer = FileOrganizer()
        
    def process_document(self, file_path, options):
        """Processa um único documento"""
        try:
            filename = os.path.basename(file_path)
            file_ext = os.path.splitext(filename)[1].lower()
            
            # Criar estrutura de saída
            doc_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            doc_output_dir = os.path.join(self.output_dir, f"doc_{doc_id}")
            os.makedirs(doc_output_dir, exist_ok=True)
            
            # Copiar original
            shutil.copy2(file_path, os.path.join(doc_output_dir, f"original{file_ext}"))
            
            results = {
                "original_file": filename,
                "processed_date": datetime.now().isoformat(),
                "output_dir": doc_output_dir,
                "extracted_text": None,
                "tables": [],
                "new_filename": None
            }
            
            # Processar baseado no tipo de arquivo
            if file_ext in ['.pdf']:
                results.update(self._process_pdf(file_path, doc_output_dir, options))
            elif file_ext in ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp']:
                results.update(self._process_image(file_path, doc_output_dir, options))
            else:
                raise ValueError(f"Formato não suportado: {file_ext}")
            
            # Extrair texto com OCR se solicitado
            if options.get('use_ocr', True):
                text = self.ocr.extract_text(file_path, options.get('language', 'por'))
                results['extracted_text'] = text
                
                # Salvar texto extraído
                text_file = os.path.join(doc_output_dir, "extracted_text.txt")
                with open(text_file, 'w', encoding='utf-8') as f:
                    f.write(text)
            
            # Extrair tabelas se solicitado
            if options.get('extract_tables', True) and file_ext == '.pdf':
                tables = self.pdf.extract_tables(file_path)
                results['tables'] = tables
                
                # Salvar tabelas em Excel
                if tables:
                    excel_file = os.path.join(doc_output_dir, "tables.xlsx")
                    self.excel.save_tables_to_excel(tables, excel_file)
            
            # Renomear arquivo se solicitado
            if options.get('rename_files', False):
                new_name = self.organizer.rename_file(
                    file_path, 
                    doc_output_dir,
                    pattern=options.get('rename_pattern', 'doc_{date}_{counter}')
                )
                results['new_filename'] = new_name
            
            # Salvar metadados
            self._save_metadata(results, doc_output_dir)
            
            return f"Processado: {len(results.get('tables', []))} tabelas extraídas"
            
        except Exception as e:
            raise Exception(f"Erro ao processar {os.path.basename(file_path)}: {str(e)}")
        finally:
            # Limpar temporários
            self._clean_temp()
    
    def _process_pdf(self, pdf_path, output_dir, options):
        """Processa arquivo PDF"""
        results = {}
        
        # Converter PDF para imagens (para OCR)
        images = convert_from_path(pdf_path, dpi=300)
        
        for i, image in enumerate(images):
            img_path = os.path.join(output_dir, f"page_{i+1}.jpg")
            image.save(img_path, 'JPEG')
        
        # Extrair texto diretamente do PDF (se for texto pesquisável)
        try:
            text = self.pdf.extract_text(pdf_path)
            if text.strip():
                with open(os.path.join(output_dir, "pdf_text.txt"), 'w', encoding='utf-8') as f:
                    f.write(text)
        except:
            pass
        
        return results
    
    def _process_image(self, image_path, output_dir, options):
        """Processa arquivo de imagem"""
        # Redimensionar e otimizar imagem
        img = Image.open(image_path)
        
        # Salvar versão otimizada
        optimized_path = os.path.join(output_dir, "optimized.jpg")
        img.save(optimized_path, 'JPEG', optimize=True, quality=85)
        
        return {}
    
    def _save_metadata(self, results, output_dir):
        """Salva metadados do processamento"""
        import json
        
        metadata_file = os.path.join(output_dir, "metadata.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            # Converter para formato serializável
            serializable = {}
            for key, value in results.items():
                if isinstance(value, (str, int, float, bool, list, dict, type(None))):
                    serializable[key] = value
                else:
                    serializable[key] = str(value)
            
            json.dump(serializable, f, indent=2, ensure_ascii=False)
    
    def _clean_temp(self):
        """Limpa arquivos temporários"""
        for file in os.listdir(self.temp_dir):
            try:
                os.remove(os.path.join(self.temp_dir, file))
            except:
                pass
    
    def batch_process_folder(self, folder_path, options):
        """Processa todos os documentos de uma pasta"""
        supported_ext = ['.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.tif']
        
        results = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in supported_ext):
                    file_path = os.path.join(root, file)
                    try:
                        result = self.process_document(file_path, options)
                        results.append((file, "Sucesso", result))
                    except Exception as e:
                        results.append((file, "Erro", str(e)))
        
        # Gerar relatório
        report_path = os.path.join(self.output_dir, "batch_report.xlsx")
        df = pd.DataFrame(results, columns=['Arquivo', 'Status', 'Detalhes'])
        df.to_excel(report_path, index=False)
        
        return results