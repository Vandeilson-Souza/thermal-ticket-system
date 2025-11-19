# 🖨️ Sistema de Impressão de Tickets Térmicos

Sistema de impressão de tickets/senhas para impressoras térmicas com suporte a QR Code e detecção automática de impressoras.

## 🚀 Instalação Rápida

### Usando o Executável (Recomendado)

1. Baixe `app.exe` 
2. Execute o arquivo
3. Acesse `http://localhost:5000`

**Pronto!** O sistema busca automaticamente por impressoras com nome "ticket-printer" ou usa a padrão do Windows.

### Usando Python

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar
python printer_app.py
```

## 📖 Endpoints da API

### Imprimir Ticket Simples
```
GET /imprimir?code=001&services=Atendimento&header=Empresa&footer=Obrigado
```

### Imprimir Ticket com QR Code
```
GET /imprimir/qrcode?code=001&services=Atendimento&header=Empresa&footer=Scan&qrcode=https://exemplo.com/001
```

## 🖨️ Configuração da Impressora

O sistema busca automaticamente por:
- Impressoras com nome contendo "ticket-printer" (maiúsculas/minúsculas)
- Se não encontrar, usa a impressora padrão do Windows

**Dica:** Compartilhe a impressora com o nome "Ticket-Printer" para detecção automática em rede.

## 🔨 Gerar Executável

```bash
python build_exe.py
```

O `app.exe` será gerado na pasta principal.

## ⚙️ Requisitos

- **Sistema:** Windows 10/11
- **Python:** 3.8+ (apenas para desenvolvimento)
- **Impressora:** Térmica 80mm (local ou compartilhada)

## 🛠️ Tecnologias

- Flask + Waitress (servidor web)
- Pillow (processamento de imagens)
- qrcode (geração de QR codes)
- pywin32 (integração Windows/impressoras)

---

**Sistema genérico para impressoras térmicas de 80mm**
