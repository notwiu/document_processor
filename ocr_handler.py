import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

class OCRHandler:
    def __init__(self):
        # Configurar caminho do Tesseract se necessário
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def extract_text(self, file_path, language='por'):
        """Extrai texto usando OCR"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return self._extract_from_pdf(file_path, language)
        elif file_ext in ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp']:
            return self._extract_from_image(file_path, language)
        else:
            raise ValueError(f"Formato não suportado para OCR: {file_ext}")
    
    def _extract_from_pdf(self, pdf_path, language):
        """Extrai texto de PDF escaneado"""
        # Converter PDF para imagens
        images = convert_from_path(pdf_path, dpi=300)
        
        text_parts = []
        for i, image in enumerate(images):
            # Pré-processamento da imagem
            processed_image = self._preprocess_image(image)
            
            # OCR
            text = pytesseract.image_to_string(
                processed_image, 
                lang=language,
                config='--psm 3 --oem 3'
            )
            text_parts.append(f"--- Página {i+1} ---\n{text}\n")
        
        return "\n".join(text_parts)
    
    def _extract_from_image(self, image_path, language):
        """Extrai texto de imagem"""
        image = Image.open(image_path)
        processed_image = self._preprocess_image(image)
        
        return pytesseract.image_to_string(
            processed_image,
            lang=language,
            config='--psm 3 --oem 3'
        )
    
    def _preprocess_image(self, image):
        """Pré-processa imagem para melhor OCR"""
        # Converter para escala de cinza
        if image.mode != 'L':
            image = image.convert('L')
        
        # Aumentar contraste
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Reduzir ruído
        import numpy as np
        img_array = np.array(image)
        
        # Limiarização adaptativa
        from PIL import ImageFilter
        image = image.filter(ImageFilter.SHARPEN)
        
        return image
    
    def get_available_languages(self):
        """Retorna idiomas disponíveis no Tesseract"""
        try:
            langs = pytesseract.get_languages()
            return langs
        except:
            return ['eng', 'por', 'spa']