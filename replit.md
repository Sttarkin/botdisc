# Discord Bot Completo - Replit Setup

## Visão Geral
Bot de Discord multifuncional com sistema de economia, níveis, mini jogos, moderação e um dashboard web de gerenciamento. Importado do GitHub e configurado para rodar no ambiente Replit.

## Estado Atual do Projeto
- **Status**: Totalmente funcional e pronto para uso
- **Última atualização**: 26 de outubro de 2025
- **Linguagem**: Python 3.11
- **Framework**: discord.py 2.6.4
- **Dashboard**: Flask 3.1.2 (porta 5000)

## Arquitetura do Projeto

### Componentes Principais
1. **Bot Discord** (`main.py`): Aplicação principal que conecta ao Discord
2. **Dashboard Web** (`dashboard.py`): Interface web Flask para gerenciar configurações
3. **Cogs/Módulos** (`cogs/`): Sistema modular de comandos
   - `basicos.py`: Comandos básicos (ping, info, ajuda)
   - `moderacao.py`: Sistema de moderação completo
   - `diversao.py`: Comandos de entretenimento
   - `jogos.py`: Mini jogos interativos
   - `economia.py`: Sistema de economia com moedas
   - `niveis.py`: Sistema de XP e níveis
   - `ia.py`: Funcionalidades com IA
   - `cargos.py`: Gerenciamento de cargos

### Estrutura de Dados
- `economia.json`: Dados de economia dos usuários (gerado automaticamente)
- `niveis.json`: Dados de níveis e XP (gerado automaticamente)
- `server_configs.json`: Configurações por servidor (gerado automaticamente)
- `config.json`: Configurações globais do bot

## Configuração no Replit

### Segredos (Secrets)
O bot usa Replit Secrets para armazenar credenciais de forma segura:
- `DISCORD_TOKEN`: Token do bot Discord (obrigatório)

### Variáveis de Ambiente
O bot lê automaticamente do `os.environ`, não necessita arquivo `.env` no Replit.

### Workflow Configurado
- **Nome**: Discord Bot
- **Comando**: `python main.py`
- **Porta**: 5000 (dashboard web)
- **Tipo**: Webview (mostra o dashboard)

## Como Funciona

### Inicialização
1. `main.py` carrega as configurações de `config.json`
2. Inicializa o bot Discord com intents necessários
3. Inicia o dashboard Flask em thread separada na porta 5000
4. Carrega todos os cogs/módulos
5. Conecta ao Discord usando o token

### Dashboard Web
- **URL**: Acessível pela porta 5000
- **Funcionalidades**:
  - Visualizar servidores do bot
  - Configurar canais habilitados
  - Definir mensagens de boas-vindas
  - Criar comandos personalizados
  - Habilitar/desabilitar módulos por servidor
  - Monitorar status do bot

### Cache Control
O dashboard está configurado com headers `no-cache` para garantir que atualizações sejam visíveis imediatamente, essencial para o ambiente Replit que mostra o site em um iframe.

## Comandos Principais

O bot usa **slash commands** (comandos com `/`):
- `/ajuda`: Central de ajuda com todos os comandos
- `/ping`: Verifica latência do bot
- `/info`: Informações sobre o bot
- `/saldo`: Mostra saldo de moedas
- `/trabalhar`: Ganha moedas trabalhando
- `/nivel`: Mostra nível e XP
- `/quiz`: Jogo de quiz
- E muitos mais...

## Arquivos Importantes

### Não Comitar (já em .gitignore)
- `.env`: Arquivo local de ambiente (não usado no Replit)
- `economia.json`: Dados de economia
- `niveis.json`: Dados de níveis
- `server_configs.json`: Configurações dos servidores
- `__pycache__/`: Cache do Python

### Configuração
- `config.json`: Configurações globais (moeda, XP, cores)
- `requirements.txt`: Dependências Python
- `.env.example`: Template de variáveis de ambiente

## Mudanças para Replit

### Alterações Realizadas
1. ✅ Instalado Python 3.11 e dependências
2. ✅ Configurado para usar Replit Secrets (DISCORD_TOKEN)
3. ✅ Re-habilitado dashboard web na porta 5000
4. ✅ Adicionado cache control headers no Flask
5. ✅ Dashboard configurado para bind em 0.0.0.0:5000
6. ✅ Criado workflow automático
7. ✅ Criado `.env.example` para documentação

### Compatibilidade
- O bot já estava configurado para usar `os.getenv('DISCORD_TOKEN')`
- `.gitignore` já estava corretamente configurado
- Estrutura modular com cogs facilita manutenção

## Preferências de Desenvolvimento

### Convenções de Código
- Código em português (comentários e mensagens)
- Uso de embeds do Discord para respostas visuais
- Sistema de permissões baseado em roles do Discord
- Tratamento de erros com mensagens amigáveis

### Banco de Dados
- Atualmente usa JSON para persistência
- Arquivos gerados automaticamente quando necessário
- Backup recomendado dos arquivos JSON periodicamente

## Próximos Passos Recomendados

1. **Adicionar bot ao servidor Discord**:
   - Ir para Discord Developer Portal
   - Copiar Client ID da aplicação
   - Usar URL: `https://discord.com/api/oauth2/authorize?client_id=SEU_CLIENT_ID&permissions=8&scope=bot%20applications.commands`

2. **Configurar permissões**:
   - Bot precisa de permissões de administrador para funcionalidades completas
   - Ou configurar permissões específicas conforme necessário

3. **Testar comandos**:
   - Usar `/ajuda` para ver todos os comandos
   - Testar sistema de economia
   - Verificar sistema de níveis

4. **Personalizar**:
   - Editar `config.json` para customizar moeda, XP, cores
   - Adicionar novos cogs em `cogs/` se necessário

## Solução de Problemas

### Bot não conecta
- Verificar se DISCORD_TOKEN está correto nos Replit Secrets
- Confirmar que o token é válido no Discord Developer Portal
- Verificar logs do console para mensagens de erro

### Dashboard não carrega
- Confirmar que a porta 5000 está acessível
- Verificar se o workflow está rodando
- Checar logs para erros do Flask

### Comandos não funcionam
- Verificar se os slash commands foram sincronizados (mensagem no console)
- Confirmar que o bot tem permissões no servidor
- Tentar usar `/ajuda` para listar comandos disponíveis

## Recursos Adicionais

- [Documentação discord.py](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Guia Rápido do Bot](GUIA_RAPIDO.md)

## Notas de Segurança

- ⚠️ Nunca compartilhar o DISCORD_TOKEN publicamente
- ⚠️ Token dá controle total sobre o bot
- ✅ Usar Replit Secrets para armazenamento seguro
- ✅ `.gitignore` configurado para proteger dados sensíveis
