import json
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        self.default_config = {
            'tesseract_path': '',  # Caminho do Tesseract-OCR
            'default_language': 'por',
            'output_format': 'xlsx',
            'auto_open_results': True,
            'keep_temp_files': False,
            'default_rename_pattern': 'doc_{date}_{counter}',
            'dpi': 300,
            'ocr_quality': 'high',  # high, medium, low
            'table_detection': True,
            'auto_organize': False
        }
        self.config = self.load_config()
    
    def load_config(self):
        """Carrega configuração do arquivo ou cria padrão"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return {**self.default_config, **json.load(f)}
            except:
                return self.default_config
        else:
            return self.default_config
    
    def save_config(self):
        """Salva configuração no arquivo"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get(self, key, default=None):
        """Obtém valor da configuração"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Define valor da configuração"""
        self.config[key] = value
        self.save_config()

# Configuração global
config = Config()