# 🎉 EXECUTÁVEL GERADO COM SUCESSO!

## 📦 Arquivos Criados

A pasta `dist\` contém tudo que você precisa:

```
📁 dist/
├── ✅ TicketPrinter.exe    (49 MB) - Executável principal
├── 📄 LEIA-ME.md                   - Manual completo
├── 🚀 INICIAR.bat                  - Atalho para iniciar
└── 📄 printer_app.exe              - Cópia do executável
```

---

## 🚀 INÍCIO RÁPIDO

### Opção 1: Usar o Batch (Mais Fácil)
1. Vá para a pasta `dist\`
2. **Dê duplo clique em `INICIAR.bat`**
3. Abra o navegador em `http://localhost:5000`

### Opção 2: Executar Direto
1. Vá para a pasta `dist\`
2. **Dê duplo clique em `TicketPrinter.exe`**
3. Abra o navegador em `http://localhost:5000`

---

## ✨ O que você pode fazer:

### 🌐 Interface Web
Acesse `http://localhost:5000` e você verá:
- ✅ Botões de teste
- ✅ Exemplos com acentos
- ✅ Testes de QR Code

### 🔗 API para Integração

**Ticket Simples:**
```
http://localhost:5000/imprimir?code=SC72&services=Emissao%20de%20Senha&header=Santa%20Casa&footer=Obrigado
```

**Ticket com QR Code:**
```
http://localhost:5000/imprimir/qrcode?code=SC72&services=Consulta&header=Hospital&footer=Aguarde&qrcode=https://site.com/SC72
```

---

## 📋 Checklist Antes de Usar

- [ ] Impressora EPSON M-T532 ligada e conectada
- [ ] Impressora configurada como padrão no Windows
- [ ] Papel térmico carregado na impressora
- [ ] Executável em uma pasta com permissão de escrita
- [ ] Porta 5000 disponível (não sendo usada)

---

## 🎯 Exemplo de Uso

1. **Execute** `INICIAR.bat` ou `TicketPrinter.exe`
2. **Veja no console:**
   ```
   🖨️  EPSON M-T532 - Sistema de Impressão
   📍 Impressora: EPSON TM-T20III
   ✅ Impressora encontrada e acessível
   Serving on http://0.0.0.0:5000
   ```
3. **Abra o navegador:** `http://localhost:5000`
4. **Clique em:** "Teste com Acentos" ou "QR Code com Acentos"
5. **Veja a mágica acontecer!** 🎉

---

## 🔧 Configurações Importantes

### ⚙️ Impressora Padrão
O sistema usa a **impressora padrão do Windows**.

**Para configurar:**
1. `Configurações` → `Impressoras`
2. Clique na EPSON M-T532
3. `Definir como padrão`

### 📁 Pasta de Trabalho
O sistema cria automaticamente uma pasta `ticket\` para:
- Salvar imagens de debug
- Armazenar previews
- Guardar arquivos temporários

---

## 💡 Dicas Importantes

### ✅ FUNCIONA:
- ✅ Tickets com texto simples
- ✅ Tickets com QR Code
- ✅ Acentos (são removidos automaticamente)
- ✅ Textos longos (quebra linha automaticamente)
- ✅ Múltiplas impressões simultâneas

### ⚠️ ATENÇÃO:
- ⚠️ O servidor fica aberto na rede local
- ⚠️ Qualquer dispositivo pode imprimir
- ⚠️ Configure firewall se necessário
- ⚠️ Feche o programa quando não usar

---

## 🆘 Problemas Comuns

### ❌ "Porta 5000 já em uso"
**Causa:** Outro programa está usando a porta  
**Solução:** Feche outros programas ou reinicie o computador

### ❌ "Impressora não encontrada"
**Causa:** Impressora não configurada como padrão  
**Solução:** Configure a EPSON como padrão no Windows

### ❌ "Nada acontece ao clicar"
**Causa:** Firewall ou antivírus bloqueando  
**Solução:** Adicione exceção no firewall/antivírus

### ❌ "QR Code cortado"
**Causa:** Papel acabando ou configuração errada  
**Solução:** Já otimizado! Troque o papel e teste novamente

---

## 📱 Integração com Sistemas Externos

### Sistema de Senhas PHP
```php
$codigo = "SC" . time();
$url = "http://localhost:5000/imprimir/qrcode";
$params = "?code=$codigo&services=Consulta%20Medica&header=Santa%20Casa&footer=Aguarde&qrcode=https://sistema.com/senha/$codigo";
file_get_contents($url . $params);
```

### Sistema Web JavaScript
```javascript
function imprimirSenha(codigo) {
    const url = `http://localhost:5000/imprimir/qrcode?` + 
                `code=${codigo}` +
                `&services=Atendimento` +
                `&header=Hospital` +
                `&footer=Aguarde` +
                `&qrcode=https://sistema.com/${codigo}`;
    fetch(url);
}
```

---

## 📊 Especificações

| Item | Valor |
|------|-------|
| **Tamanho do Executável** | ~49 MB |
| **Porta do Servidor** | 5000 |
| **Largura do Papel** | 80mm |
| **Resolução** | 576 pixels |
| **QR Code** | 200x200 px |
| **Altura Máxima** | 1500 pixels |
| **Encoding** | UTF-8 → CP860 |

---

## 🎁 Extras Incluídos

Na pasta raiz você também tem:
- `test_ticket_preview.py` - Gera previews visuais
- `visualizar_previews.html` - Visualiza previews no navegador
- `build_exe.py` - Script usado para gerar o .exe

---

## 📞 Suporte

**Problemas técnicos?**
1. Verifique o console (janela preta) para mensagens de erro
2. Leia o `LEIA-ME.md` completo
3. Teste com os exemplos da página inicial

---

## ✅ PRONTO PARA USAR!

1. **Vá para:** `dist\`
2. **Execute:** `INICIAR.bat` ou `TicketPrinter.exe`
3. **Acesse:** `http://localhost:5000`
4. **Imprima!** 🎉

---

**Desenvolvido com ❤️ para impressão de senhas**  
**Sistema otimizado para EPSON M-T532**

🖨️ **Boas impressões!** 🖨️
