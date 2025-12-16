import pdfplumber
import PyPDF2
import pandas as pd
from pdf2image import convert_from_path
import os

class PDFHandler:
    def __init__(self):
        # Configurar caminho do poppler (ADICIONE ESTAS LINHAS)
        self.poppler_path = None
        
        # Verificar caminhos comuns no Windows
        possible_paths = [
            r'C:\poppler\Library\bin',
            r'C:\Program Files\poppler\Library\bin',
            r'C:\Users\{}\AppData\Local\Programs\poppler\Library\bin'.format(os.getlogin())
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                self.poppler_path = path
                break
    
    def _convert_pdf_to_images(self, pdf_path, output_dir):
        """Converte PDF para imagens com caminho do poppler"""
        try:
            images = convert_from_path(
                pdf_path, 
                dpi=300,
                poppler_path=self.poppler_path  # Passar o caminho aqui
            )
            
            for i, image in enumerate(images):
                img_path = os.path.join(output_dir, f"page_{i+1}.jpg")
                image.save(img_path, 'JPEG', quality=95)
                
            return len(images)
        except Exception as e:
            print(f"Erro ao converter PDF para imagens: {e}")
            print(f"Caminho do poppler: {self.poppler_path}")
            return 0