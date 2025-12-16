import os
import shutil
from datetime import datetime
import re

class FileOrganizer:
    def __init__(self):
        self.counter = 1
    
    def rename_file(self, file_path, output_dir, pattern='doc_{date}_{counter}'):
        """Renomeia arquivo baseado em padrão"""
        filename = os.path.basename(file_path)
        file_ext = os.path.splitext(filename)[1]
        
        # Substituir placeholders no padrão
        new_name = pattern
        
        # {date} - data atual
        if '{date}' in pattern:
            date_str = datetime.now().strftime("%Y%m%d")
            new_name = new_name.replace('{date}', date_str)
        
        # {counter} - contador incremental
        if '{counter}' in pattern:
            new_name = new_name.replace('{counter}', str(self.counter).zfill(3))
            self.counter += 1
        
        # {original} - nome original (sem extensão)
        if '{original}' in pattern:
            original_name = os.path.splitext(filename)[0]
            new_name = new_name.replace('{original}', original_name)
        
        # {time} - hora atual
        if '{time}' in pattern:
            time_str = datetime.now().strftime("%H%M%S")
            new_name = new_name.replace('{time}', time_str)
        
        # Adicionar extensão
        new_filename = f"{new_name}{file_ext}"
        new_path = os.path.join(output_dir, new_filename)
        
        # Copiar arquivo com novo nome
        shutil.copy2(file_path, new_path)
        
        return new_filename
    
    def organize_by_type(self, folder_path):
        """Organiza arquivos por tipo em subpastas"""
        file_types = {
            'PDFs': ['.pdf'],
            'Imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif'],
            'Documentos': ['.doc', '.docx', '.txt', '.rtf'],
            'Planilhas': ['.xls', '.xlsx', '.csv'],
            'Outros': []
        }
        
        # Criar pastas
        for folder_name in file_types.keys():
            os.makedirs(os.path.join(folder_path, folder_name), exist_ok=True)
        
        # Mover arquivos
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            if os.path.isfile(file_path):
                file_ext = os.path.splitext(filename)[1].lower()
                moved = False
                
                for folder_name, extensions in file_types.items():
                    if file_ext in extensions:
                        shutil.move(file_path, os.path.join(folder_path, folder_name, filename))
                        moved = True
                        break
                
                if not moved:
                    shutil.move(file_path, os.path.join(folder_path, 'Outros', filename))
        
        return "Arquivos organizados por tipo"
    
    def batch_rename(self, folder_path, pattern):
        """Renomeia todos os arquivos de uma pasta em lote"""
        results = []
        
        for i, filename in enumerate(sorted(os.listdir(folder_path)), 1):
            file_path = os.path.join(folder_path, filename)
            
            if os.path.isfile(file_path):
                new_name = pattern.replace('{n}', str(i).zfill(3))
                new_name = new_name.replace('{name}', os.path.splitext(filename)[0])
                
                file_ext = os.path.splitext(filename)[1]
                new_filename = f"{new_name}{file_ext}"
                new_path = os.path.join(folder_path, new_filename)
                
                os.rename(file_path, new_path)
                results.append((filename, new_filename))
        
        return results
    
    def find_duplicates(self, folder_path):
        """Encontra arquivos duplicados por conteúdo"""
        import hashlib
        
        hashes = {}
        duplicates = []
        
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                # Calcular hash MD5 do arquivo
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                
                if file_hash in hashes:
                    duplicates.append((file_path, hashes[file_hash]))
                else:
                    hashes[file_hash] = file_path
        
        return duplicates