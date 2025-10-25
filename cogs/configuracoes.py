import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime

class Configuracoes(commands.Cog):
    """Sistema de configurações por servidor"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config_file = 'server_configs.json'
        self.configs = self.load_configs()
    
    def load_configs(self):
        """Carregar configurações dos servidores"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_configs(self):
        """Salvar configurações dos servidores"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.configs, f, indent=2, ensure_ascii=False)
    
    def get_guild_config(self, guild_id):
        """Obter configurações de um servidor"""
        guild_id = str(guild_id)
        if guild_id not in self.configs:
            self.configs[guild_id] = {
                'enabled_channels': [],
                'welcome_channel': None,
                'welcome_message': 'Bem-vindo ao servidor, {user}!',
                'custom_commands': {},
                'ai_enabled': True,
                'moderation_enabled': True,
                'economy_enabled': True,
                'levels_enabled': True
            }
            self.save_configs()
        return self.configs[guild_id]
    
    def is_channel_allowed(self, guild_id, channel_id):
        """Verificar se um canal é permitido para o bot"""
        config = self.get_guild_config(guild_id)
        enabled_channels = config.get('enabled_channels', [])
        
        # Se não há canais específicos configurados, permitir em todos
        if not enabled_channels:
            return True
        
        return str(channel_id) in enabled_channels
    
    def is_feature_enabled(self, guild_id, feature):
        """Verificar se uma funcionalidade está habilitada"""
        config = self.get_guild_config(guild_id)
        return config.get(feature, True)
    
    def get_custom_commands(self, guild_id):
        """Obter comandos personalizados de um servidor"""
        config = self.get_guild_config(guild_id)
        return config.get('custom_commands', {})
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Verificar comandos personalizados e restrições de canal"""
        # Ignorar mensagens do bot
        if message.author == self.bot.user:
            return
        
        # Ignorar DMs
        if not message.guild:
            return
        
        guild_id = str(message.guild.id)
        channel_id = str(message.channel.id)
        
        # Verificar se o canal é permitido
        if not self.is_channel_allowed(guild_id, channel_id):
            return
        
        # Verificar se a IA está habilitada para DMs automáticas
        if isinstance(message.channel, discord.DMChannel):
            if not self.is_feature_enabled(guild_id, 'ai_enabled'):
                return
        
        # Nota: comandos customizados agora são executados via slash commands (/comando)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Enviar mensagem de boas-vindas"""
        guild_id = str(member.guild.id)
        config = self.get_guild_config(guild_id)
        
        welcome_channel_id = config.get('welcome_channel')
        if not welcome_channel_id:
            return
        
        welcome_channel = self.bot.get_channel(int(welcome_channel_id))
        if not welcome_channel:
            return
        
        welcome_message = config.get('welcome_message', 'Bem-vindo ao servidor, {user}!')
        
        # Substituir variáveis
        welcome_message = welcome_message.replace('{user}', member.mention)
        welcome_message = welcome_message.replace('{server}', member.guild.name)
        
        # Criar embed de boas-vindas
        embed = discord.Embed(
            title="🎉 Boas-vindas!",
            description=welcome_message,
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"ID: {member.id}")
        
        await welcome_channel.send(embed=embed)
    
    @app_commands.command(name='config', description='Mostrar configurações do servidor')
    @app_commands.checks.has_permissions(administrator=True)
    async def config_slash(self, interaction: discord.Interaction):
        """Mostrar configurações do servidor via slash"""
        guild = interaction.guild
        guild_id = str(guild.id)
        config = self.get_guild_config(guild_id)

        embed = discord.Embed(
            title="⚙️ Configurações do Servidor",
            color=discord.Color.blue()
        )

        features = [
            ("🤖 IA (Aziel)", config.get('ai_enabled', True)),
            ("🛡️ Moderação", config.get('moderation_enabled', True)),
            ("💰 Economia", config.get('economy_enabled', True)),
            ("📈 Níveis", config.get('levels_enabled', True))
        ]

        for feature, enabled in features:
            status = "✅ Habilitado" if enabled else "❌ Desabilitado"
            embed.add_field(name=feature, value=status, inline=True)

        welcome_channel = config.get('welcome_channel')
        if welcome_channel:
            channel = self.bot.get_channel(int(welcome_channel))
            welcome_text = f"📺 {channel.mention}" if channel else "❌ Canal não encontrado"
        else:
            welcome_text = "❌ Não configurado"

        embed.add_field(name="Boas-vindas", value=welcome_text, inline=False)

        enabled_channels = config.get('enabled_channels', [])
        if enabled_channels:
            channels_text = ""
            for channel_id in enabled_channels[:5]:
                channel = self.bot.get_channel(int(channel_id))
                if channel:
                    channels_text += f"📺 {channel.mention}\n"
            if len(enabled_channels) > 5:
                channels_text += f"... e mais {len(enabled_channels) - 5} canais"
        else:
            channels_text = "🌐 Todos os canais"

        embed.add_field(name="Canais Permitidos", value=channels_text, inline=False)

        custom_commands = config.get('custom_commands', {})
        if custom_commands:
            commands_text = ""
            for name, command in list(custom_commands.items())[:3]:
                usage_count = command.get('usage_count', 0)
                commands_text += f"`/{name}` ({usage_count} usos)\n"
            if len(custom_commands) > 3:
                commands_text += f"... e mais {len(custom_commands) - 3} comandos"
        else:
            commands_text = "Nenhum comando personalizado"

        embed.add_field(name="Comandos Personalizados", value=commands_text, inline=False)

        await interaction.response.send_message(embed=embed)
    
    @commands.command(name='dashboard')
    @commands.has_permissions(administrator=True)
    async def dashboard_command(self, ctx):
        """Mostrar link para o dashboard"""
        embed = discord.Embed(
            title="🌐 Dashboard Web",
            description="Configure o bot através do dashboard web!",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="� Observação",
            value="O dashboard web foi removido. Use os comandos de configuração via Discord (slash commands) para gerenciar o bot.",
            inline=False
        )
        embed.set_footer(text="Acesso restrito a administradores")
        await ctx.send(embed=embed)

    @app_commands.command(name='dashboard', description='Informação sobre o dashboard (removido)')
    @app_commands.checks.has_permissions(administrator=True)
    async def dashboard_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🌐 Dashboard Web",
            description="O dashboard web foi removido. Todas as configurações agora são feitas por comandos no Discord.",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Como configurar",
            value="Use `/config`, `/set_welcome_channel`, `/add_custom_command`, `/remove_custom_command`, etc.",
            inline=False
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='set_welcome_channel', description='Define o canal de boas-vindas do servidor')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(channel='Canal de boas-vindas')
    async def set_welcome_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_id = str(interaction.guild.id)
        config = self.get_guild_config(guild_id)
        config['welcome_channel'] = str(channel.id)
        self.save_configs()
        await interaction.response.send_message(f"✅ Canal de boas-vindas definido para {channel.mention}")

    @app_commands.command(name='set_welcome_message', description='Define a mensagem de boas-vindas (use {user} e {server})')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(message='Mensagem de boas-vindas (use {user} e {server})')
    async def set_welcome_message(self, interaction: discord.Interaction, message: str):
        guild_id = str(interaction.guild.id)
        config = self.get_guild_config(guild_id)
        config['welcome_message'] = message
        self.save_configs()
        await interaction.response.send_message("✅ Mensagem de boas-vindas atualizada.")

    @app_commands.command(name='add_custom_command', description='Adiciona um comando personalizado ao servidor')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(name='Nome do comando (sem /)', response='Resposta (use {user}, {server}, {channel})')
    async def add_custom_command(self, interaction: discord.Interaction, name: str, response: str):
        guild_id = str(interaction.guild.id)
        config = self.get_guild_config(guild_id)
        custom = config.get('custom_commands', {})
        name = name.lower()
        custom[name] = {'response': response, 'usage_count': 0}
        config['custom_commands'] = custom
        self.save_configs()
        await interaction.response.send_message(f"✅ Comando `/{name}` adicionado.")

    @app_commands.command(name='remove_custom_command', description='Remove um comando personalizado')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(name='Nome do comando a remover')
    async def remove_custom_command(self, interaction: discord.Interaction, name: str):
        guild_id = str(interaction.guild.id)
        config = self.get_guild_config(guild_id)
        custom = config.get('custom_commands', {})
        name = name.lower()
        if name in custom:
            del custom[name]
            config['custom_commands'] = custom
            self.save_configs()
            await interaction.response.send_message(f"✅ Comando `/{name}` removido.")
        else:
            await interaction.response.send_message(f"❌ Comando `/{name}` não existe.", ephemeral=True)

    @app_commands.command(name='list_custom_commands', description='Lista comandos personalizados do servidor')
    @app_commands.checks.has_permissions(administrator=True)
    async def list_custom_commands(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        custom = self.get_custom_commands(guild_id)
        if not custom:
            await interaction.response.send_message("Nenhum comando personalizado configurado.", ephemeral=True)
            return
        texto = "\n".join(f"/{name} ({data.get('usage_count',0)} usos)" for name, data in custom.items())
        await interaction.response.send_message(f"Comandos personalizados:\n{texto}")

    @app_commands.command(name='run_command', description='Executa um comando personalizado do servidor')
    @app_commands.describe(name='Nome do comando')
    async def run_command(self, interaction: discord.Interaction, name: str):
        guild_id = str(interaction.guild.id)
        custom = self.get_custom_commands(guild_id)
        name = name.lower()
        if name not in custom:
            await interaction.response.send_message(f"❌ Comando `/{name}` não encontrado.", ephemeral=True)
            return
        command = custom[name]
        # Incrementar uso
        command['usage_count'] = command.get('usage_count', 0) + 1
        self.save_configs()

        response = command['response']
        response = response.replace('{user}', interaction.user.mention)
        response = response.replace('{server}', interaction.guild.name)
        response = response.replace('{channel}', interaction.channel.mention)

        await interaction.response.send_message(response)

    @app_commands.command(name='set_feature', description='Habilita ou desabilita uma feature do bot no servidor')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(feature='Funcionalidade (ai/moderation/economy/levels)', enabled='True para habilitar, False para desabilitar')
    async def set_feature(self, interaction: discord.Interaction, feature: str, enabled: bool):
        guild_id = str(interaction.guild.id)
        feature_map = {
            'ai': 'ai_enabled',
            'moderation': 'moderation_enabled',
            'economy': 'economy_enabled',
            'levels': 'levels_enabled'
        }
        key = feature_map.get(feature.lower())
        if not key:
            await interaction.response.send_message("❌ Feature inválida. Use ai/moderation/economy/levels", ephemeral=True)
            return
        config = self.get_guild_config(guild_id)
        config[key] = bool(enabled)
        self.save_configs()
        await interaction.response.send_message(f"✅ Feature `{feature}` definida para {enabled}")

    @app_commands.command(name='allow_channel', description='Adiciona um canal à lista de canais permitidos para o bot')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(channel='Canal a permitir')
    async def allow_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_id = str(interaction.guild.id)
        config = self.get_guild_config(guild_id)
        lst = config.get('enabled_channels', [])
        if str(channel.id) in lst:
            await interaction.response.send_message('Canal já está permitido.', ephemeral=True)
            return
        lst.append(str(channel.id))
        config['enabled_channels'] = lst
        self.save_configs()
        await interaction.response.send_message(f'✅ Canal {channel.mention} permitido para uso do bot')

    @app_commands.command(name='disallow_channel', description='Remove um canal da lista de canais permitidos')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(channel='Canal a remover')
    async def disallow_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_id = str(interaction.guild.id)
        config = self.get_guild_config(guild_id)
        lst = config.get('enabled_channels', [])
        if str(channel.id) not in lst:
            await interaction.response.send_message('Canal não está na lista.', ephemeral=True)
            return
        lst.remove(str(channel.id))
        config['enabled_channels'] = lst
        self.save_configs()
        await interaction.response.send_message(f'✅ Canal {channel.mention} removido da lista de permitidos')

async def setup(bot):
    await bot.add_cog(Configuracoes(bot))

