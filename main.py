import discord
from discord.ext import commands
import os
import json
import asyncio
import threading
import time
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Carregar configurações
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.reactions = True

# Criar bot
bot = commands.Bot(
    command_prefix=None,
    intents=intents,
    help_command=None,  # Vamos criar nosso próprio comando de ajuda
    description='Bot de Discord completo com jogos e diversão!'
)

@bot.event
async def on_ready():
    """Evento quando o bot está online"""
    print(f'╔══════════════════════════════════════╗')
    print(f'║  Bot conectado com sucesso!          ║')
    print(f'║  Nome: {bot.user.name:<26}    ║')
    print(f'║  ID: {bot.user.id:<28}    ║')
    print(f'║  Servidores: {len(bot.guilds):<23} ║')
    print(f'╚══════════════════════════════════════╝')
    
    # Definir status
    await bot.change_presence(
        activity=discord.Game(name=f"/ajuda | {len(bot.guilds)} servidores"),
        status=discord.Status.online
    )

    # Tentar sincronizar slash commands (app commands)
    try:
        await bot.tree.sync()
        print('[OK] Slash commands sincronizados')
    except Exception as e:
        print(f'[WARN] Erro ao sincronizar slash commands: {e}')

@bot.event
async def on_guild_join(guild):
    """Evento quando o bot entra em um servidor"""
    print(f'[+] Bot adicionado ao servidor: {guild.name} (ID: {guild.id})')
    await bot.change_presence(
        activity=discord.Game(name=f"/ajuda | {len(bot.guilds)} servidores")
    )

@bot.event
async def on_guild_remove(guild):
    """Evento quando o bot sai de um servidor"""
    print(f'[-] Bot removido do servidor: {guild.name} (ID: {guild.id})')
    await bot.change_presence(
        activity=discord.Game(name=f"/ajuda | {len(bot.guilds)} servidores")
    )

@bot.event
async def on_command_error(ctx, error):
    """Tratamento de erros"""
    # Ignorar erros que já foram tratados pelos cogs
    if hasattr(ctx.command, 'on_error'):
        return
    
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="❌ Comando não encontrado",
            description=f"Use `/ajuda` para ver todos os comandos disponíveis.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="🚫 Sem permissão",
            description="Você não tem permissão para usar este comando!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ Argumento faltando",
            description=f"Uso correto: Use os parâmetros do slash command conforme mostrado no Discord",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="⏰ Cooldown",
            description=f"Aguarde {error.retry_after:.1f} segundos antes de usar este comando novamente.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
    
    else:
        print(f'Erro: {error}')

async def load_cogs():
    """Carregar todos os cogs"""
    cogs = [
        'cogs.configuracoes',
        'cogs.basicos',
        'cogs.moderacao',
        'cogs.diversao',
        'cogs.jogos',
        'cogs.economia',
        'cogs.niveis',
        'cogs.ia'
    ]
    
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f'[OK] Cog carregado: {cog}')
        except Exception as e:
            print(f'[ERRO] Erro ao carregar {cog}: {e}')

async def main():
    """Função principal"""
    # Definir tempo de início
    bot.start_time = time.time()
    
    # Nota: dashboard web removido — configuração passa a ser feita via comandos no Discord
    
    async with bot:
        await load_cogs()
        await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    asyncio.run(main())

