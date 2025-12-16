# 🧠 DocFlow Pro
### Software Profissional de Processamento de Documentos em PDF

O **DocFlow Pro** é um aplicativo desktop desenvolvido em **Python** para automatizar o processamento de documentos PDF, combinando **OCR, extração de tabelas e organização de arquivos** em uma interface moderna, simples e profissional.

Projetado para quem precisa **ganhar tempo**, **reduzir erros manuais** e **padronizar documentos**.

---

## 🎯 Público-alvo

- Escritórios de contabilidade  
- Setor financeiro e administrativo  
- Escritórios jurídicos  
- Empresas que digitalizam documentos  
- Profissionais autônomos  
- Pequenas e médias empresas  

---

## ✨ Funcionalidades

### 📄 Processamento de PDFs
- OCR para PDFs escaneados
- Extração de texto para arquivos `.txt`
- Extração automática de tabelas para **Excel (.xlsx)**

### ⚙️ Automação
- Processamento de múltiplos PDFs
- Execução em segundo plano (interface não trava)
- Barra de progresso e status em tempo real

### 🖥️ Interface Gráfica
- Interface moderna (CustomTkinter)
- Modo escuro
- Layout com sidebar
- Preview do texto extraído
- Feedback visual profissional

### 🔐 Licenciamento
- Tela de login com chave de licença
- Estrutura pronta para expansão (licença online, expiração, por máquina, etc.)

---

## 🧩 Como funciona

1. Inicie o aplicativo  
2. Insira uma licença válida  
3. Selecione um ou mais arquivos PDF  
4. Escolha o tipo de processamento:
   - OCR (TXT)
   - Tabelas (Excel)
5. O sistema processa e salva os arquivos automaticamente

---

## 📁 Arquivos Gerados

| Documento | Resultado |
|---------|----------|
| PDF escaneado | `.txt` |
| PDF estruturado com tabelas | `.xlsx` |
| Ambos | `.txt` + `.xlsx` |

> ⚠️ **Observação:**  
> A extração de tabelas funciona apenas em **PDFs estruturados (digitais)**.  
> PDFs escaneados geram apenas OCR em texto.

---

## 🛠️ Tecnologias Utilizadas

- Python 3  
- CustomTkinter  
- Tesseract OCR  
- pdf2image  
- Camelot  
- Pandas  

---

## 📦 Instalação (Modo Desenvolvimento)

### 1️⃣ Clonar o projeto
```bash
git clone https://github.com/seu-usuario/docflow-pro.git
cd docflow-pro