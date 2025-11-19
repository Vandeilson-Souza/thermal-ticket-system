# 🖨️ Sistema de Impressão de Tickets - EPSON M-T532

Sistema de impressão de tickets/senhas para impressoras térmicas EPSON M-T532 com suporte a QR Code.

## 📦 Arquivos do Projeto

- `printer_app.py` - Código fonte principal
- `printer_app.spec` - Arquivo de configuração para compilar
- `printer_app.exe` - Executável pronto (na pasta dist/)
- `requirements.txt` - Dependências Python
- `README.md` - Este arquivo

## 🚀 Como Usar

### Opção 1: Executável (Recomendado)

1. Baixe o arquivo `printer_app.exe` da pasta `dist/`
2. Execute o arquivo
3. Acesse `http://localhost:5000` no navegador

### Opção 2: Via Python

```bash
pip install -r requirements.txt
python printer_app.py
```

## 📖 API

### Imprimir Ticket Simples
```
GET /imprimir?code=SC72&services=Emissao%20de%20Senha&header=Santa%20Casa&footer=Bem-vindo
```

### Imprimir Ticket com QR Code
```
GET /imprimir/qrcode?code=SC72&services=Emissao%20de%20Senha&header=Santa%20Casa&footer=Scan%20o%20QR&qrcode=https://exemplo.com/SC72
```

## 🔧 Compilar Executável

Para gerar o arquivo .exe:

```bash
pip install pyinstaller
pyinstaller printer_app.spec
```

O executável será criado em `dist/printer_app.exe`

## ⚙️ Requisitos

- Windows 10/11
- Python 3.8+ (apenas para executar via código)
- Impressora EPSON M-T532 configurada como padrão

## 🛠️ Tecnologias

- Python + Flask
- Pillow (processamento de imagens)
- qrcode (geração de QR codes)
- pywin32 (integração com Windows)

---

**Desenvolvido para EPSON M-T532**
