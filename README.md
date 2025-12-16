# document_processor# 📄 Document Processor Pro

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

**Processador Inteligente de Documentos** que extrai texto, tabelas e automatiza tarefas com interface gráfica moderna.

![Screenshot da Interface](https://via.placeholder.com/800x450/2b2b2b/ffffff?text=Document+Processor+Pro+UI)

## ✨ **Funcionalidades**

### 🔤 **Extração de Texto**
- OCR em múltiplos idiomas (Português, Inglês, Espanhol, Francês)
- Suporte a PDFs escaneados e imagens (JPG, PNG, TIFF)
- Pré-processamento automático para melhor qualidade

### 📊 **Processamento de Tabelas**
- Extração automática de tabelas de PDFs
- Exportação para Excel com formatação profissional
- Detecção inteligente de estrutura de dados

### 🔄 **Automação**
- Renomeação em lote com padrões personalizáveis
- Processamento de pastas inteiras
- Interface arrasta e solta intuitiva

### 🎨 **Interface Moderna**
- Tema escuro profissional
- Feedback visual em tempo real
- Monitoramento de recursos do sistema
- Logs coloridos e organizados

## 🚀 **Instalação Rápida**

### Pré-requisitos
- Python 3.8 ou superior
- Tesseract OCR instalado

### Passo a Passo
```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/document-processor.git
cd document-processor

# 2. Crie ambiente virtual (opcional mas recomendado)
python -m venv .venv

# 3. Ative o ambiente virtual
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# 4. Instale dependências
pip install -r requirements.txt

# 5. Configure o Tesseract OCR
# Baixe os arquivos de idioma em:
# https://github.com/tesseract-ocr/tessdata
# Coloque em: C:\Program Files\Tesseract-OCR\tessdata\

# 6. Execute o programa
python main.py