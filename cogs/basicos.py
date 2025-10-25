import discord
from discord import app_commands
from discord.ext import commands
import json
import time
import platform
import psutil
from datetime import datetime

class Basicos(commands.Cog):
    """Comandos básicos do bot"""
    
    def __init__(self, bot):
        self.bot = bot
        with open('config.json', 'r', encoding='utf-8') as f:
            self.config = json.load(f)
    
    # (prefix commands removed) Ping is now available as a slash command `/ping`

    # Slash command equivalent
    @app_commands.command(name='ping', description='Mostra a latência do bot')
    async def ping_slash(self, interaction: discord.Interaction):
        """Mostra a latência do bot (slash)"""
        start = time.time()
        await interaction.response.defer()
        end = time.time()

        latencia_api = round(self.bot.latency * 1000, 2)
        latencia_msg = round((end - start) * 1000, 2)

        embed = discord.Embed(
            title="🏓 Pong!",
            color=discord.Color.blue()
        )
        embed.add_field(name="📡 Latência da API", value=f"`{latencia_api}ms`", inline=True)
        embed.add_field(name="💬 Latência da Mensagem", value=f"`{latencia_msg}ms`", inline=True)
        embed.timestamp = datetime.utcnow()

        await interaction.followup.send(embed=embed)
    
    # (prefix commands removed) Info is now available as a slash command `/info`

    @app_commands.command(name='info', description='Informações sobre o bot')
    async def info_slash(self, interaction: discord.Interaction):
        await interaction.response.defer()
        ram_usada = psutil.Process().memory_info().rss / 1024 ** 2  # MB
        cpu_uso = psutil.Process().cpu_percent(interval=1)
        total_membros = sum(guild.member_count for guild in self.bot.guilds)

        embed = discord.Embed(
            title="🤖 Informações do Bot",
            description="Bot de Discord completo com jogos, economia e muito mais!",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="📊 Estatísticas",
            value=f"```\n"
                  f"Servidores: {len(self.bot.guilds)}\n"
                  f"Usuários: {total_membros}\n"
                  f"Comandos: {len(self.bot.commands)}\n"
                  f"```",
            inline=True
        )

        embed.add_field(
            name="💻 Sistema",
            value=f"```\n"
                  f"Python: {platform.python_version()}\n"
                  f"Discord.py: {discord.__version__}\n"
                  f"RAM: {ram_usada:.2f} MB\n"
                  f"CPU: {cpu_uso}%\n"
                  f"```",
            inline=True
        )

        embed.add_field(
            name="🔧 Informações",
            value=f"```\n"
                  f"Prefix: {self.config['prefix']}\n"
                  f"Latência: {round(self.bot.latency * 1000)}ms\n"
                  f"```",
            inline=False
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Solicitado por {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        embed.timestamp = datetime.utcnow()

        await interaction.followup.send(embed=embed)
    
    # (prefix commands removed) Ajuda é agora `/ajuda`

    @app_commands.command(name='ajuda', description='Mostra todos os comandos disponíveis')
    @app_commands.describe(categoria='Categoria específica (opcional)')
    async def ajuda_slash(self, interaction: discord.Interaction, categoria: str = None):
        prefix = self.config['prefix']
        await interaction.response.defer()

        if categoria is None:
            embed = discord.Embed(
                title="📚 Central de Ajuda",
                description=f"Use `/ajuda <categoria>` para ver comandos específicos\n\n"
                           f"**Categorias disponíveis:**",
                color=discord.Color.blue()
            )

            categorias = {
                "basicos": "📌 Comandos básicos do bot",
                "moderacao": "🛡️ Comandos de moderação",
                "diversao": "🎉 Comandos de diversão",
                "jogos": "🎮 Mini jogos interativos",
                "economia": "💰 Sistema de economia",
                "niveis": "📊 Sistema de níveis e XP"
            }

            for cat, desc in categorias.items():
                embed.add_field(
                    name=f"`/{cat}`",
                    value=desc,
                    inline=False
                )

            embed.set_footer(text=f"Total de comandos: {len(self.bot.commands)}")
        else:
            categoria = categoria.lower()
            cog_map = {
                'basicos': 'Basicos',
                'moderacao': 'Moderacao',
                'diversao': 'Diversao',
                'jogos': 'Jogos',
                'economia': 'Economia',
                'niveis': 'Niveis'
            }

            if categoria not in cog_map:
                await interaction.followup.send(f"❌ Categoria `{categoria}` não encontrada!")
                return

            cog = self.bot.get_cog(cog_map[categoria])
            if not cog:
                await interaction.followup.send(f"❌ Categoria `{categoria}` não está carregada!")
                return

            embed = discord.Embed(
                title=f"📚 Ajuda - {categoria.capitalize()}",
                description=cog.__doc__,
                color=discord.Color.blue()
            )

            for command in cog.get_commands():
                aliases = f" ({', '.join(command.aliases)})" if command.aliases else ""
                embed.add_field(
                    name=f"`{prefix}{command.name}{aliases}`",
                    value=command.help or "Sem descrição",
                    inline=False
                )

        await interaction.followup.send(embed=embed)
    
    # (prefix commands removed) Serverinfo é agora `/serverinfo`

    @app_commands.command(name='serverinfo', description='Informações sobre o servidor')
    async def serverinfo_slash(self, interaction: discord.Interaction):
        guild = interaction.guild
        await interaction.response.defer()

        online = sum(1 for m in guild.members if m.status == discord.Status.online)
        idle = sum(1 for m in guild.members if m.status == discord.Status.idle)
        dnd = sum(1 for m in guild.members if m.status == discord.Status.dnd)
        offline = sum(1 for m in guild.members if m.status == discord.Status.offline)

        embed = discord.Embed(
            title=f"📊 Informações - {guild.name}",
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

        embed.add_field(
            name="👑 Dono",
            value=guild.owner.mention,
            inline=True
        )

        embed.add_field(
            name="📅 Criado em",
            value=guild.created_at.strftime("%d/%m/%Y"),
            inline=True
        )

        embed.add_field(
            name="🆔 ID",
            value=f"`{guild.id}`",
            inline=True
        )

        embed.add_field(
            name=f"👥 Membros ({guild.member_count})",
            value=f"🟢 {online} | 🟡 {idle} | 🔴 {dnd} | ⚫ {offline}",
            inline=False
        )

        embed.add_field(
            name="📝 Canais",
            value=f"💬 Texto: {len(guild.text_channels)}\n"
                  f"🔊 Voz: {len(guild.voice_channels)}",
            inline=True
        )

        embed.add_field(
            name="😃 Emojis",
            value=f"{len(guild.emojis)}/{guild.emoji_limit}",
            inline=True
        )

        embed.add_field(
            name="🎭 Cargos",
            value=len(guild.roles),
            inline=True
        )

        embed.set_footer(text=f"Solicitado por {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        embed.timestamp = datetime.utcnow()

        await interaction.followup.send(embed=embed)
    
    # (prefix commands removed) Userinfo é agora `/userinfo`

    @app_commands.command(name='userinfo', description='Informações sobre um usuário')
    @app_commands.describe(member='Usuário a ser consultado (opcional)')
    async def userinfo_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        await interaction.response.defer()
        member = member or interaction.user

        status_emoji = {
            discord.Status.online: "🟢 Online",
            discord.Status.idle: "🟡 Ausente",
            discord.Status.dnd: "🔴 Não Perturbe",
            discord.Status.offline: "⚫ Offline"
        }

        embed = discord.Embed(
            title=f"👤 {member.name}",
            color=member.color
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(
            name="📛 Nome Completo",
            value=f"{member.name}#{member.discriminator}",
            inline=True
        )

        embed.add_field(
            name="🆔 ID",
            value=f"`{member.id}`",
            inline=True
        )

        embed.add_field(
            name="📊 Status",
            value=status_emoji.get(member.status, "❓ Desconhecido"),
            inline=True
        )

        embed.add_field(
            name="📅 Conta Criada",
            value=member.created_at.strftime("%d/%m/%Y às %H:%M"),
            inline=False
        )

        embed.add_field(
            name="📥 Entrou no Servidor",
            value=member.joined_at.strftime("%d/%m/%Y às %H:%M"),
            inline=False
        )

        roles = [role.mention for role in member.roles[1:]]  # Excluir @everyone
        if roles:
            embed.add_field(
                name=f"🎭 Cargos ({len(roles)})",
                value=" ".join(roles[:10]) + ("..." if len(roles) > 10 else ""),
                inline=False
            )

        embed.set_footer(text=f"Solicitado por {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        embed.timestamp = datetime.utcnow()

        await interaction.followup.send(embed=embed)
    
    # (prefix commands removed) Avatar é agora `/avatar`

    @app_commands.command(name='avatar', description='Mostra o avatar de um usuário')
    @app_commands.describe(member='Usuário (opcional)')
    async def avatar_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        await interaction.response.defer()
        member = member or interaction.user

        embed = discord.Embed(
            title=f"🖼️ Avatar de {member.name}",
            color=member.color
        )

        embed.set_image(url=member.display_avatar.url)
        embed.add_field(
            name="🔗 Links",
            value=f"[PNG]({member.display_avatar.with_format('png').url}) | "
                  f"[JPG]({member.display_avatar.with_format('jpg').url}) | "
                  f"[WEBP]({member.display_avatar.with_format('webp').url})",
            inline=False
        )

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Basicos(bot))

