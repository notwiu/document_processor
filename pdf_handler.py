import pdfplumber
import PyPDF2
import pandas as pd

class PDFHandler:
    def __init__(self):
        pass
    
    def extract_text(self, pdf_path):
        """Extrai texto de PDF pesquisável"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text() + "\n\n"
        except Exception as e:
            print(f"Erro ao extrair texto do PDF: {e}")
        
        return text
    
    def extract_tables(self, pdf_path):
        """Extrai tabelas de PDF"""
        tables = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()
                    
                    if page_tables:
                        for i, table in enumerate(page_tables):
                            # Converter para DataFrame
                            df = pd.DataFrame(table)
                            
                            # Limpar DataFrame
                            df = self._clean_dataframe(df)
                            
                            if not df.empty:
                                table_info = {
                                    'page': page_num + 1,
                                    'table_number': i + 1,
                                    'dataframe': df,
                                    'shape': df.shape,
                                    'columns': df.columns.tolist()
                                }
                                tables.append(table_info)
        except Exception as e:
            print(f"Erro ao extrair tabelas: {e}")
        
        return tables
    
    def _clean_dataframe(self, df):
        """Limpa e formata DataFrame"""
        if df.empty:
            return df
        
        # Remover linhas completamente vazias
        df = df.dropna(how='all')
        
        # Remover colunas completamente vazias
        df = df.dropna(axis=1, how='all')
        
        # Resetar índice
        df = df.reset_index(drop=True)
        
        # Usar primeira linha como cabeçalho se apropriado
        if df.shape[0] > 1:
            # Verificar se a primeira linha parece ser cabeçalho
            first_row = df.iloc[0]
            second_row = df.iloc[1] if df.shape[0] > 1 else None
            
            # Heurística simples: se a primeira linha tem strings e a segunda tem números/mistura
            if second_row is not None:
                df.columns = [str(col).strip() for col in first_row]
                df = df[1:].reset_index(drop=True)
        
        return df
    
    def get_pdf_info(self, pdf_path):
        """Obtém informações do PDF"""
        info = {}
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                info['pages'] = len(reader.pages)
                info['encrypted'] = reader.is_encrypted
                if reader.metadata:
                    info.update(reader.metadata)
        except Exception as e:
            print(f"Erro ao obter informações do PDF: {e}")
        
        return info