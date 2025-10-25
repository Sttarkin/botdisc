# 🚀 Guia Rápido de Instalação

## Passo a Passo para Iniciantes

### 1️⃣ Instalar Python
1. Baixe Python 3.8+ em: https://www.python.org/downloads/
2. Durante a instalação, **marque** "Add Python to PATH"
3. Clique em "Install Now"

### 2️⃣ Criar o Bot no Discord

1. Acesse: https://discord.com/developers/applications
2. Clique em **"New Application"**
3. Dê um nome ao bot e clique em **"Create"**
4. No menu lateral, clique em **"Bot"**
5. Clique em **"Add Bot"** → **"Yes, do it!"**
6. Em **"Privileged Gateway Intents"**, ative:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
7. Clique em **"Reset Token"** e copie o token (guarde em local seguro!)

### 3️⃣ Adicionar o Bot ao Servidor

1. No menu lateral, clique em **"OAuth2"** → **"URL Generator"**
2. Em **SCOPES**, marque:
   - ✅ bot
   - ✅ applications.commands
3. Em **BOT PERMISSIONS**, marque:
   - ✅ Administrator (ou selecione permissões específicas)
4. Copie a URL gerada no final da página
5. Cole a URL no navegador e adicione o bot ao seu servidor

### 4️⃣ Configurar o Bot

1. Abra a pasta `botdisc` no terminal/cmd
2. Crie um arquivo chamado `.env` (sem nome antes do ponto)
3. Abra o arquivo `.env` e adicione:
```
DISCORD_TOKEN=seu_token_aqui
```
   (Substitua `seu_token_aqui` pelo token copiado no passo 2)

### 5️⃣ Instalar Dependências

Abra o terminal na pasta do bot e execute:

**Windows:**
```bash
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
pip3 install -r requirements.txt
```

### 6️⃣ Iniciar o Bot

Execute no terminal:

**Windows:**
```bash
python main.py
```

**Linux/Mac:**
```bash
python3 main.py
```

Se tudo der certo, você verá:
```
╔══════════════════════════════════════╗
║  Bot conectado com sucesso!          ║
║  Nome: SeuBot                        ║
║  ID: 123456789                       ║
║  Servidores: 1                       ║
╚══════════════════════════════════════╝
```

### 7️⃣ Testar o Bot

No Discord, digite:
```
!ping
```

Se o bot responder, está funcionando! 🎉

## ⚙️ Configurações Opcionais

Edite `config.json` para personalizar:
- Prefixo dos comandos (padrão: `!`)
- Nome da moeda
- XP por mensagem
- E muito mais!

## 🆘 Problemas Comuns

### "discord.py não encontrado"
Execute: `pip install discord.py`

### "Token inválido"
- Verifique se copiou o token corretamente
- Verifique se não há espaços extras no arquivo `.env`

### "Bot não responde"
- Verifique se os Intents estão ativados no Developer Portal
- Confirme que o bot está online no servidor

## 📚 Próximos Passos

- Leia o `README.md` completo para ver todos os comandos
- Digite `!ajuda` no Discord para explorar as funcionalidades
- Personalize o bot editando os arquivos em `cogs/`

## 🎮 Comandos Essenciais para Começar

```
!ajuda          - Ver todos os comandos
!ping           - Testar latência
!daily          - Ganhar moedas diárias
!trabalhar      - Trabalhar por moedas
!adivinhar      - Jogar adivinhação
!ppt pedra      - Jogar pedra-papel-tesoura
```

**Divirta-se! 🚀**

