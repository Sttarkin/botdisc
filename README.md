# 🤖 Bot de Discord Completo

Um bot de Discord completo e multifuncional com sistema de economia, níveis, mini jogos e muito mais!

## 📋 Índice

- [Características](#-características)
- [Instalação](#-instalação)
- [Configuração](#️-configuração)
- [Comandos](#-comandos)
- [Sistema de Permissões](#-sistema-de-permissões)
- [Suporte](#-suporte)

## ✨ Características

### 🎮 **Mini Jogos Interativos**
- Pedra, Papel ou Tesoura
- Jogo de Adivinhação
- Quiz de Conhecimentos Gerais
- Jogo da Velha (PvP)
- Corrida de Moedas

### 💰 **Sistema de Economia**
- Trabalhar para ganhar moedas
- Recompensas diárias
- Loja com itens colecionáveis
- Sistema de inventário
- Transferência de moedas entre usuários
- Banco para depositar e sacar
- Apostas e roubos

### 📊 **Sistema de Níveis e XP**
- Ganhe XP enviando mensagens
- Sistema de níveis progressivo
- Ranking do servidor
- Notificações de level up

### 🛡️ **Moderação Completa**
- Ban, Kick e Warn
- Mute/Unmute com cargo automático
- Limpeza de mensagens
- Modo lento (slowmode)
- Trancar/Destrancar canais

### 🎉 **Comandos de Diversão**
- Dado personalizado
- Cara ou coroa
- 8ball (bola mágica)
- Piadas e fatos interessantes
- Shipômetro
- Conversores de texto (emoji, inverter, mock)
- Contagem regressiva

### 📌 **Comandos Básicos**
- Ping e latência
- Informações do bot
- Informações do servidor
- Informações de usuários
- Sistema de ajuda completo
- Avatar

## 🚀 Instalação

### Requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### Passo 1: Clone o repositório
```bash
git clone <url-do-repositorio>
cd botdisc
```

### Passo 2: Instale as dependências
```bash
pip install -r requirements.txt
```

### Passo 3: Configure o bot
1. Crie uma aplicação no [Discord Developer Portal](https://discord.com/developers/applications)
2. Crie um bot e copie o token
3. Crie um arquivo `.env` na raiz do projeto:
```env
DISCORD_TOKEN=seu_token_aqui
```

### Passo 4: Inicie o bot
```bash
python main.py
```

## ⚙️ Configuração

Edite o arquivo `config.json` para personalizar o bot:

```json
{
  "prefix": "!",                    // Prefixo dos comandos
  "cor_principal": "0x7289DA",      // Cor principal dos embeds
  "moeda_nome": "Coins",            // Nome da moeda
  "moeda_emoji": "💰",              // Emoji da moeda
  "xp_por_mensagem": 15,            // XP base por mensagem
  "xp_variacao": 10,                // Variação do XP
  "cooldown_xp": 60,                // Cooldown de XP (segundos)
  "nivel_base": 100,                // XP base para nível 1
  "multiplicador_nivel": 1.5        // Multiplicador de XP por nível
}
```

## 📝 Comandos

### 📌 Comandos Básicos

| Comando | Aliases | Descrição |
|---------|---------|-----------|
| `!ping` | `latencia` | Mostra a latência do bot |
| `!info` | `botinfo`, `sobre` | Informações sobre o bot |
| `!ajuda` | `help`, `comandos` | Central de ajuda |
| `!serverinfo` | `infoserver` | Informações do servidor |
| `!userinfo` | `infouser` | Informações de um usuário |
| `!avatar` | `av` | Mostra o avatar de um usuário |

### 🛡️ Comandos de Moderação

| Comando | Aliases | Descrição | Permissão |
|---------|---------|-----------|-----------|
| `!kick <membro> [motivo]` | `expulsar` | Expulsa um membro | Expulsar Membros |
| `!ban <membro> [motivo]` | `banir` | Bane um membro | Banir Membros |
| `!unban <id>` | `desbanir` | Desbane um usuário | Banir Membros |
| `!clear [quantidade]` | `limpar`, `purge` | Limpa mensagens (1-100) | Gerenciar Mensagens |
| `!mute <membro> [motivo]` | `mutar`, `silenciar` | Silencia um membro | Gerenciar Cargos |
| `!unmute <membro>` | `desmutar` | Remove silenciamento | Gerenciar Cargos |
| `!warn <membro> [motivo]` | `avisar`, `advertir` | Avisa um membro | Gerenciar Mensagens |
| `!slowmode [segundos]` | `lento` | Define modo lento | Gerenciar Canais |
| `!lock` | `trancar` | Tranca o canal | Gerenciar Canais |
| `!unlock` | `destrancar` | Destranca o canal | Gerenciar Canais |

### 🎉 Comandos de Diversão

| Comando | Aliases | Descrição |
|---------|---------|-----------|
| `!dado [lados]` | `roll`, `rolar` | Rola um dado |
| `!moeda` | `coinflip`, `cara_coroa` | Joga uma moeda |
| `!escolher <opções>` | `choose`, `selecionar` | Escolhe uma opção |
| `!8ball <pergunta>` | `bola8` | Pergunta à bola 8 mágica |
| `!piada` | `joke` | Conta uma piada |
| `!fato` | `fact`, `curiosidade` | Mostra um fato interessante |
| `!ship <pessoa1> <pessoa2>` | `shippar` | Shipômetro |
| `!emoji <texto>` | `emojify` | Converte texto em emojis |
| `!reverse <texto>` | `inverter` | Inverte o texto |
| `!mock <texto>` | `zombar` | Transforma em mOcKiNg TeXt |
| `!contador [segundos]` | `count` | Contagem regressiva |

### 🎮 Mini Jogos

| Comando | Aliases | Descrição |
|---------|---------|-----------|
| `!ppt <escolha>` | `pedrapapeltesoura`, `jokenpo` | Pedra, Papel ou Tesoura |
| `!adivinhar` | `guess`, `adivinha` | Adivinhe o número (1-100) |
| `!quiz` | `trivia` | Quiz de conhecimentos |
| `!velha <oponente>` | `tictactoe`, `jogodavelha` | Jogo da Velha (PvP) |
| `!coinrace` | `corrida_moedas` | Corrida de moedas |

### 💰 Sistema de Economia

| Comando | Aliases | Descrição |
|---------|---------|-----------|
| `!saldo [membro]` | `bal`, `balance`, `dinheiro` | Mostra o saldo |
| `!trabalhar` | `work`, `trabalho` | Trabalhe por moedas (1h cooldown) |
| `!daily` | `diario` | Recompensa diária (24h cooldown) |
| `!loja` | `shop`, `store` | Mostra a loja |
| `!comprar <emoji>` | `buy` | Compra um item |
| `!inventario [membro]` | `inv`, `inventory` | Mostra o inventário |
| `!dar <membro> <quantidade>` | `give`, `doar` | Dá moedas para outro usuário |
| `!depositar <quantidade>` | `dep`, `deposit` | Deposita no banco |
| `!sacar <quantidade>` | `withdraw`, `saque` | Saca do banco |
| `!apostar <quantidade>` | `bet` | Aposte suas moedas (50% chance) |
| `!roubar <membro>` | `rob`, `steal` | Tente roubar (30% chance, 1h cooldown) |

### 📊 Sistema de Níveis

| Comando | Aliases | Descrição |
|---------|---------|-----------|
| `!nivel [membro]` | `level`, `rank`, `xp` | Mostra nível e XP |
| `!leaderboard [página]` | `lb`, `top`, `ranking` | Ranking do servidor |
| `!setlevel <membro> <nivel>` | `setnivel` | Define nível (Admin) |
| `!addxp <membro> <xp>` | `addexp` | Adiciona XP (Admin) |
| `!resetlevel [membro]` | `resetnivel` | Reseta níveis (Admin) |

## 🔐 Sistema de Permissões

### Comandos de Moderação
- **Kick/Ban**: Requer permissão "Expulsar Membros" ou "Banir Membros"
- **Clear**: Requer permissão "Gerenciar Mensagens"
- **Mute/Unmute**: Requer permissão "Gerenciar Cargos"
- **Slowmode/Lock/Unlock**: Requer permissão "Gerenciar Canais"

### Comandos de Administrador
- **SetLevel/AddXP/ResetLevel**: Requer permissão "Administrador"

## 📊 Estrutura do Projeto

```
botdisc/
│
├── main.py              # Arquivo principal do bot
├── config.json          # Configurações do bot
├── requirements.txt     # Dependências
├── .env                 # Token do bot (NÃO COMMITAR!)
├── .env.example         # Exemplo do arquivo .env
│
├── cogs/                # Módulos do bot
│   ├── basicos.py       # Comandos básicos
│   ├── moderacao.py     # Comandos de moderação
│   ├── diversao.py      # Comandos de diversão
│   ├── jogos.py         # Mini jogos
│   ├── economia.py      # Sistema de economia
│   └── niveis.py        # Sistema de níveis
│
├── economia.json        # Dados da economia (gerado automaticamente)
└── niveis.json          # Dados de níveis (gerado automaticamente)
```

## 🎨 Personalização

### Adicionar Novos Comandos
1. Edite o arquivo correspondente em `cogs/`
2. Use o decorador `@commands.command()`
3. Reinicie o bot

### Adicionar Itens à Loja
Edite o dicionário `loja_itens` em `cogs/economia.py`:
```python
'🎮': {
    'nome': 'Nome do Item',
    'preco': 5000,
    'descricao': 'Descrição do item'
}
```

### Adicionar Perguntas ao Quiz
Edite a lista `quiz_perguntas` em `cogs/jogos.py`:
```python
{
    "pergunta": "Sua pergunta?",
    "opcoes": ["Opção 1", "Opção 2", "Opção 3", "Opção 4"],
    "resposta": 1  # Índice da resposta correta (0-3)
}
```

## 🐛 Solução de Problemas

### O bot não responde
- Verifique se o token está correto no arquivo `.env`
- Confirme que o bot tem as permissões necessárias no servidor
- Verifique se os Intents estão habilitados no Developer Portal

### Comandos de moderação não funcionam
- Verifique se o cargo do bot está acima dos cargos que ele tenta moderar
- Confirme que o bot tem as permissões necessárias

### Erros ao iniciar
- Certifique-se de que todas as dependências estão instaladas: `pip install -r requirements.txt`
- Verifique se está usando Python 3.8 ou superior

## 📝 Notas Importantes

- **Segurança**: NUNCA compartilhe seu token do bot! Adicione `.env` ao `.gitignore`
- **Backup**: Faça backup regular dos arquivos `economia.json` e `niveis.json`
- **Rate Limits**: O Discord limita requisições. Cooldowns ajudam a evitar problemas

## 🔄 Atualizações Futuras

- [ ] Comandos de música (play, pause, skip)
- [ ] Sistema de warnings persistente
- [ ] Logs de moderação
- [ ] Sistema de tickets
- [ ] Auto-moderação (anti-spam, anti-raid)
- [ ] Dashboard web
- [ ] Mais mini jogos

## 📜 Licença

Este projeto é de código aberto e está disponível para uso pessoal e educacional.

## 👨‍💻 Desenvolvedor

Bot criado com ❤️ usando discord.py

## 🆘 Suporte

Se encontrar bugs ou tiver sugestões, abra uma issue no repositório!

---

**Divirta-se usando o bot! 🎉**

