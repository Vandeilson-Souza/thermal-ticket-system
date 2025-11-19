# 🖨️ Ticket Printer - Sistema de Impressão de Senhas

## ✅ Executável Gerado com Sucesso!

**Arquivo:** `TicketPrinter.exe`  
**Tamanho:** ~49 MB  
**Localização:** `dist\TicketPrinter.exe`

---

## 🚀 Como Usar

### 1️⃣ Pré-requisitos
- ✅ Windows 7/8/10/11
- ✅ Impressora térmica EPSON M-T532 (ou compatível)
- ✅ Impressora configurada como padrão no Windows

### 2️⃣ Instalação
1. Copie o arquivo `TicketPrinter.exe` para qualquer pasta
2. Não precisa instalar nada - é um executável único!

### 3️⃣ Executar o Sistema
1. **Dê duplo clique** em `TicketPrinter.exe`
2. Uma janela de terminal irá abrir mostrando:
   ```
   🖨️  EPSON M-T532 - Sistema de Impressão
   📍 Impressora: [Nome da sua impressora]
   ✅ Impressora encontrada e acessível
   Serving on http://0.0.0.0:5000
   ```
3. **Abra seu navegador** e acesse: `http://localhost:5000`

### 4️⃣ Usar o Sistema

#### 🌐 Interface Web (Recomendado)
Acesse `http://localhost:5000` no navegador para:
- Ver a interface de testes
- Imprimir tickets de exemplo
- Testar com acentos e QR codes

#### 🔗 API para Integração

**Imprimir Ticket Simples:**
```
http://localhost:5000/imprimir?code=SC72&services=Emissao%20de%20Senha&header=Santa%20Casa&footer=Obrigado!
```

**Imprimir Ticket com QR Code:**
```
http://localhost:5000/imprimir/qrcode?code=SC72&services=Consulta%20Medica&header=Santa%20Casa&footer=Aguarde&qrcode=https://site.com/ticket/SC72
```

#### 📋 Parâmetros Disponíveis

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `code` | Código da senha | `SC72` |
| `services` | Descrição dos serviços | `Emissao%20de%20Senha` |
| `header` | Cabeçalho/Título | `Santa%20Casa%20de%20Tiete` |
| `footer` | Rodapé | `Seja%20bem-vindo(a)` |
| `qrcode` | Dados para QR Code | `https://site.com/SC72` |
| `created_date` | Data/hora | `07/11/2025%2010:18` |

💡 **Dica:** Use `%20` para espaços nas URLs

---

## ✨ Recursos

✅ **Impressão ESC/POS Nativa** - Comandos diretos para impressora térmica  
✅ **Fallback para Imagem** - Se ESC/POS falhar, usa bitmap  
✅ **QR Code Integrado** - Gera QR codes automaticamente  
✅ **Suporte a Acentos** - Remove acentos para compatibilidade  
✅ **Layout Profissional** - Código em destaque, linhas separadoras  
✅ **Corte Automático** - Corta o papel automaticamente após impressão  

---

## 🔧 Configuração da Impressora

### Windows 10/11:
1. `Configurações` → `Dispositivos` → `Impressoras e Scanners`
2. Clique na sua impressora EPSON M-T532
3. Clique em `Gerenciar` → `Definir como padrão`

### Windows 7/8:
1. `Painel de Controle` → `Dispositivos e Impressoras`
2. Clique com botão direito na EPSON M-T532
3. `Definir como impressora padrão`

---

## 📁 Estrutura de Arquivos

Quando você executa o `TicketPrinter.exe`, ele cria automaticamente:

```
📁 [Pasta do executável]
├── 📄 TicketPrinter.exe    ← Executável principal
└── 📁 ticket/               ← Criada automaticamente
    ├── debug_*.png          ← Imagens de debug
    ├── print_*.bmp          ← Arquivos temporários
    └── preview_*.png        ← Previews (se usar teste)
```

---

## 🧪 Testar o Sistema

### Método 1: Interface Web
1. Execute `TicketPrinter.exe`
2. Acesse `http://localhost:5000`
3. Clique nos botões de teste

### Método 2: URL Direta no Navegador
```
http://localhost:5000/imprimir?code=TESTE123&services=Teste&header=TESTE&footer=OK
```

### Método 3: Script de Teste Python
```python
import requests

# Imprimir ticket simples
requests.get('http://localhost:5000/imprimir', params={
    'code': 'SC72',
    'services': 'Emissão de Senha',
    'header': 'Santa Casa',
    'footer': 'Obrigado!'
})
```

---

## ❓ Solução de Problemas

### ❌ "Impressora não encontrada"
**Solução:**
- Verifique se a impressora está ligada
- Configure a impressora como padrão no Windows
- Reinstale o driver da impressora

### ❌ "Porta 5000 já em uso"
**Solução:**
- Feche outros programas que usam a porta 5000
- Ou edite o código para usar outra porta

### ❌ "QR Code cortado"
**Solução:**
- O sistema já foi otimizado para não cortar
- Avança 8-10 linhas antes do corte
- Usa altura de até 1500px

### ❌ "Acentos não aparecem"
**Solução:**
- O sistema remove acentos automaticamente
- Isso é normal para impressoras térmicas
- Use URLs com `%20` para espaços e `%` para caracteres especiais

---

## 🔒 Segurança

⚠️ **IMPORTANTE:**
- O servidor roda em `0.0.0.0:5000` (todas as interfaces)
- Qualquer computador na rede pode acessar
- Use firewall se necessário
- Não exponha para a internet pública

---

## 📞 Integração com Outros Sistemas

### PHP
```php
$url = 'http://localhost:5000/imprimir/qrcode?';
$params = http_build_query([
    'code' => 'SC72',
    'services' => 'Consulta Médica',
    'header' => 'Santa Casa',
    'footer' => 'Aguarde ser chamado',
    'qrcode' => 'https://site.com/ticket/SC72'
]);
file_get_contents($url . $params);
```

### JavaScript
```javascript
fetch('http://localhost:5000/imprimir/qrcode?' + new URLSearchParams({
    code: 'SC72',
    services: 'Consulta Médica',
    header: 'Santa Casa',
    footer: 'Aguarde',
    qrcode: 'https://site.com/ticket/SC72'
}));
```

### C#
```csharp
using (var client = new HttpClient())
{
    var url = "http://localhost:5000/imprimir/qrcode?code=SC72&services=Consulta&header=Santa%20Casa&footer=Aguarde&qrcode=https://site.com/SC72";
    var response = await client.GetAsync(url);
}
```

---

## 📊 Especificações Técnicas

- **Largura do Papel:** 80mm
- **Resolução:** 576 pixels (8 dots/mm)
- **Altura Máxima:** 1500 pixels
- **QR Code:** 200x200 pixels
- **Encoding:** CP860 (para ESC/POS)
- **Formato Imagem:** 1-bit Bitmap
- **Corte:** Parcial (Partial Cut)

---

## 📝 Changelog

### Versão Atual
✅ Código em DESTAQUE (tamanho maior, negrito)  
✅ QR code otimizado (não corta mais)  
✅ Suporte a acentos via URL  
✅ Avanço de 8-10 linhas antes do corte  
✅ Altura dinâmica até 1500px  
✅ Fallback automático ESC/POS → Bitmap  

---

## 👨‍💻 Desenvolvedor

Sistema de Impressão para EPSON M-T532  
Desenvolvido com Python, Flask, Pillow, QRCode  
Compilado com PyInstaller  

---

## 📄 Licença

Este software é fornecido "como está", sem garantias.  
Use por sua conta e risco.

---

**🎉 Pronto para usar! Execute o TicketPrinter.exe e comece a imprimir!**
