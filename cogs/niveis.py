import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import math
from datetime import datetime, timedelta
import random

class Niveis(commands.Cog):
    """Sistema de níveis e experiência"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db_file = 'niveis.json'
        self.load_data()
        
        with open('config.json', 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.cooldowns = {}  # Cooldown de XP por usuário
    
    def load_data(self):
        """Carrega os dados de níveis"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {}
    
    def save_data(self):
        """Salva os dados de níveis"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
    
    def get_user_data(self, guild_id, user_id):
        """Obtém os dados de um usuário"""
        guild_id = str(guild_id)
        user_id = str(user_id)
        
        if guild_id not in self.data:
            self.data[guild_id] = {}
        
        if user_id not in self.data[guild_id]:
            self.data[guild_id][user_id] = {
                'xp': 0,
                'nivel': 1,
                'mensagens': 0
            }
            self.save_data()
        
        return self.data[guild_id][user_id]
    
    def calcular_xp_necessario(self, nivel):
        """Calcula o XP necessário para o próximo nível"""
        base = self.config['nivel_base']
        multiplicador = self.config['multiplicador_nivel']
        return int(base * (nivel ** multiplicador))
    
    def calcular_nivel(self, xp):
        """Calcula o nível baseado no XP total"""
        nivel = 1
        while xp >= self.calcular_xp_necessario(nivel):
            xp -= self.calcular_xp_necessario(nivel)
            nivel += 1
        return nivel, xp
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Evento que dá XP quando usuários mandam mensagens"""
        # Ignorar bots e DMs
        if message.author.bot or not message.guild:
            return
        
        # Verificar cooldown
        user_key = f"{message.guild.id}_{message.author.id}"
        agora = datetime.now()
        
        if user_key in self.cooldowns:
            ultimo = self.cooldowns[user_key]
            diferenca = (agora - ultimo).total_seconds()
            if diferenca < self.config['cooldown_xp']:
                return
        
        self.cooldowns[user_key] = agora
        
        # Dar XP
        dados = self.get_user_data(message.guild.id, message.author.id)
        xp_base = self.config['xp_por_mensagem']
        variacao = self.config['xp_variacao']
        xp_ganho = random.randint(xp_base - variacao, xp_base + variacao)
        
        nivel_anterior = dados['nivel']
        dados['xp'] += xp_ganho
        dados['mensagens'] += 1
        
        # Calcular novo nível
        nivel_atual, xp_restante = self.calcular_nivel(dados['xp'])
        
        if nivel_atual > nivel_anterior:
            # Subiu de nível!
            dados['nivel'] = nivel_atual
            dados['xp'] = xp_restante
            self.save_data()
            
            embed = discord.Embed(
                title="🎉 Level Up!",
                description=f"Parabéns {message.author.mention}! Você subiu para o **Nível {nivel_atual}**!",
                color=discord.Color.gold()
            )
            embed.set_thumbnail(url=message.author.display_avatar.url)
            
            await message.channel.send(embed=embed)
        else:
            dados['xp'] = xp_restante
            self.save_data()
    
    @commands.command(name='nivel', aliases=['level', 'rank', 'xp'])
    async def nivel(self, ctx, membro: discord.Member = None):
        """Mostra o nível e XP de um usuário"""
        membro = membro or ctx.author
        dados = self.get_user_data(ctx.guild.id, membro.id)
        
        nivel = dados['nivel']
        xp_atual = dados['xp']
        xp_necessario = self.calcular_xp_necessario(nivel)
        
        # Calcular porcentagem
        porcentagem = int((xp_atual / xp_necessario) * 100)
        barra_cheia = int(porcentagem / 10)
        barra_vazia = 10 - barra_cheia
        barra = "█" * barra_cheia + "░" * barra_vazia
        
        embed = discord.Embed(
            title=f"📊 Perfil de {membro.display_name}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=membro.display_avatar.url)
        
        embed.add_field(name="🏆 Nível", value=f"**{nivel}**", inline=True)
        embed.add_field(name="💬 Mensagens", value=f"**{dados['mensagens']}**", inline=True)
        embed.add_field(name="⭐ XP", value=f"**{xp_atual}** / {xp_necessario}", inline=True)
        
        embed.add_field(
            name="Progresso",
            value=f"`{barra}` {porcentagem}%",
            inline=False
        )
        
        # Calcular XP total
        xp_total = sum(self.calcular_xp_necessario(n) for n in range(1, nivel)) + xp_atual
        embed.set_footer(text=f"XP Total: {xp_total}")
        
        await ctx.send(embed=embed)

    @app_commands.command(name='nivel', description='Mostra o nível e XP de um usuário')
    @app_commands.describe(membro='Membro (opcional)')
    async def nivel_slash(self, interaction: discord.Interaction, membro: discord.Member = None):
        membro = membro or interaction.user
        dados = self.get_user_data(interaction.guild.id, membro.id)
        nivel = dados['nivel']
        xp_atual = dados['xp']
        xp_necessario = self.calcular_xp_necessario(nivel)
        porcentagem = int((xp_atual / xp_necessario) * 100) if xp_necessario > 0 else 0
        barra_cheia = int(porcentagem / 10)
        barra_vazia = 10 - barra_cheia
        barra = "█" * barra_cheia + "░" * barra_vazia
        embed = discord.Embed(title=f"📊 Perfil de {membro.display_name}", color=discord.Color.blue())
        embed.set_thumbnail(url=membro.display_avatar.url)
        embed.add_field(name="🏆 Nível", value=f"**{nivel}**", inline=True)
        embed.add_field(name="💬 Mensagens", value=f"**{dados['mensagens']}**", inline=True)
        embed.add_field(name="⭐ XP", value=f"**{xp_atual}** / {xp_necessario}", inline=True)
        embed.add_field(name="Progresso", value=f"`{barra}` {porcentagem}%", inline=False)
        xp_total = sum(self.calcular_xp_necessario(n) for n in range(1, nivel)) + xp_atual
        embed.set_footer(text=f"XP Total: {xp_total}")
        await interaction.response.send_message(embed=embed)
    
    @commands.command(name='leaderboard', aliases=['lb', 'top', 'ranking'])
    async def leaderboard(self, ctx, pagina: int = 1):
        """Mostra o ranking de níveis do servidor"""
        if pagina < 1:
            pagina = 1
        
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.data or not self.data[guild_id]:
            await ctx.send("❌ Ainda não há dados de níveis neste servidor!")
            return
        
        # Ordenar usuários por XP total
        usuarios = []
        for user_id, dados in self.data[guild_id].items():
            xp_total = sum(self.calcular_xp_necessario(n) for n in range(1, dados['nivel'])) + dados['xp']
            usuarios.append({
                'id': int(user_id),
                'nivel': dados['nivel'],
                'xp': dados['xp'],
                'xp_total': xp_total
            })
        
        usuarios.sort(key=lambda x: x['xp_total'], reverse=True)
        
        # Paginação
        por_pagina = 10
        total_paginas = math.ceil(len(usuarios) / por_pagina)
        pagina = min(pagina, total_paginas)
        
        inicio = (pagina - 1) * por_pagina
        fim = inicio + por_pagina
        
        embed = discord.Embed(
            title=f"🏆 Ranking de Níveis - {ctx.guild.name}",
            description=f"Página {pagina}/{total_paginas}",
            color=discord.Color.gold()
        )
        
        for i, usuario in enumerate(usuarios[inicio:fim], inicio + 1):
            try:
                member = await ctx.guild.fetch_member(usuario['id'])
                
                # Medalhas para top 3
                if i == 1:
                    medalha = "🥇"
                elif i == 2:
                    medalha = "🥈"
                elif i == 3:
                    medalha = "🥉"
                else:
                    medalha = f"`#{i}`"
                
                embed.add_field(
                    name=f"{medalha} {member.display_name}",
                    value=f"Nível: **{usuario['nivel']}** | XP Total: **{usuario['xp_total']}**",
                    inline=False
                )
            except:
                continue
        
        # Mostrar posição do autor
        for i, usuario in enumerate(usuarios, 1):
            if usuario['id'] == ctx.author.id:
                embed.set_footer(text=f"Sua posição: #{i}")
                break
        
        await ctx.send(embed=embed)

    @app_commands.command(name='leaderboard', description='Mostra o ranking de níveis do servidor')
    @app_commands.describe(pagina='Número da página')
    async def leaderboard_slash(self, interaction: discord.Interaction, pagina: int = 1):
        if pagina < 1:
            pagina = 1
        guild_id = str(interaction.guild.id)
        if guild_id not in self.data or not self.data[guild_id]:
            await interaction.response.send_message("❌ Ainda não há dados de níveis neste servidor!", ephemeral=True)
            return
        usuarios = []
        for user_id, dados in self.data[guild_id].items():
            xp_total = sum(self.calcular_xp_necessario(n) for n in range(1, dados['nivel'])) + dados['xp']
            usuarios.append({'id': int(user_id), 'nivel': dados['nivel'], 'xp': dados['xp'], 'xp_total': xp_total})
        usuarios.sort(key=lambda x: x['xp_total'], reverse=True)
        por_pagina = 10
        total_paginas = math.ceil(len(usuarios) / por_pagina)
        pagina = min(pagina, total_paginas)
        inicio = (pagina - 1) * por_pagina
        fim = inicio + por_pagina
        embed = discord.Embed(title=f"🏆 Ranking de Níveis - {interaction.guild.name}", description=f"Página {pagina}/{total_paginas}", color=discord.Color.gold())
        for i, usuario in enumerate(usuarios[inicio:fim], inicio + 1):
            try:
                member = await interaction.guild.fetch_member(usuario['id'])
                if i == 1:
                    medalha = "🥇"
                elif i == 2:
                    medalha = "🥈"
                elif i == 3:
                    medalha = "🥉"
                else:
                    medalha = f"`#{i}`"
                embed.add_field(name=f"{medalha} {member.display_name}", value=f"Nível: **{usuario['nivel']}** | XP Total: **{usuario['xp_total']}**", inline=False)
            except:
                continue
        for i, usuario in enumerate(usuarios, 1):
            if usuario['id'] == interaction.user.id:
                embed.set_footer(text=f"Sua posição: #{i}")
                break
        await interaction.response.send_message(embed=embed)
    
    @commands.command(name='setlevel', aliases=['setnivel'])
    @commands.has_permissions(administrator=True)
    async def setlevel(self, ctx, membro: discord.Member, nivel: int):
        """Define o nível de um usuário (Apenas Administradores)"""
        if nivel < 1:
            await ctx.send("❌ O nível deve ser maior que 0!")
            return
        
        if nivel > 100:
            await ctx.send("❌ O nível máximo é 100!")
            return
        
        dados = self.get_user_data(ctx.guild.id, membro.id)
        dados['nivel'] = nivel
        dados['xp'] = 0
        self.save_data()
        
        embed = discord.Embed(
            title="✅ Nível Definido",
            description=f"O nível de {membro.mention} foi definido para **{nivel}**!",
            color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)

    @app_commands.command(name='setlevel', description='Define o nível de um usuário (Administrador)')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(membro='Membro', nivel='Nível a definir')
    async def setlevel_slash(self, interaction: discord.Interaction, membro: discord.Member, nivel: int):
        if nivel < 1:
            await interaction.response.send_message("❌ O nível deve ser maior que 0!", ephemeral=True)
            return
        if nivel > 100:
            await interaction.response.send_message("❌ O nível máximo é 100!", ephemeral=True)
            return
        dados = self.get_user_data(interaction.guild.id, membro.id)
        dados['nivel'] = nivel
        dados['xp'] = 0
        self.save_data()
        embed = discord.Embed(title="✅ Nível Definido", description=f"O nível de {membro.mention} foi definido para **{nivel}**!", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)
    
    @commands.command(name='addxp', aliases=['addexp'])
    @commands.has_permissions(administrator=True)
    async def addxp(self, ctx, membro: discord.Member, quantidade: int):
        """Adiciona XP a um usuário (Apenas Administradores)"""
        if quantidade <= 0:
            await ctx.send("❌ A quantidade deve ser maior que 0!")
            return
        
        dados = self.get_user_data(ctx.guild.id, membro.id)
        nivel_anterior = dados['nivel']
        dados['xp'] += quantidade
        
        # Recalcular nível
        nivel_atual, xp_restante = self.calcular_nivel(dados['xp'])
        dados['nivel'] = nivel_atual
        dados['xp'] = xp_restante
        self.save_data()
        
        embed = discord.Embed(
            title="✅ XP Adicionado",
            description=f"{membro.mention} recebeu **{quantidade} XP**!",
            color=discord.Color.green()
        )
        
        if nivel_atual > nivel_anterior:
            embed.add_field(
                name="🎉 Level Up!",
                value=f"Nível {nivel_anterior} → Nível {nivel_atual}",
                inline=False
            )
        
        await ctx.send(embed=embed)

    @app_commands.command(name='addxp', description='Adiciona XP a um usuário (Administrador)')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(membro='Membro', quantidade='Quantidade de XP a adicionar')
    async def addxp_slash(self, interaction: discord.Interaction, membro: discord.Member, quantidade: int):
        if quantidade <= 0:
            await interaction.response.send_message("❌ A quantidade deve ser maior que 0!", ephemeral=True)
            return
        dados = self.get_user_data(interaction.guild.id, membro.id)
        nivel_anterior = dados['nivel']
        dados['xp'] += quantidade
        nivel_atual, xp_restante = self.calcular_nivel(dados['xp'])
        dados['nivel'] = nivel_atual
        dados['xp'] = xp_restante
        self.save_data()
        embed = discord.Embed(title="✅ XP Adicionado", description=f"{membro.mention} recebeu **{quantidade} XP**!", color=discord.Color.green())
        if nivel_atual > nivel_anterior:
            embed.add_field(name="🎉 Level Up!", value=f"Nível {nivel_anterior} → Nível {nivel_atual}", inline=False)
        await interaction.response.send_message(embed=embed)
    
    @commands.command(name='resetlevel', aliases=['resetnivel'])
    @commands.has_permissions(administrator=True)
    async def resetlevel(self, ctx, membro: discord.Member = None):
        """Reseta o nível de um usuário ou do servidor inteiro (Apenas Administradores)"""
        if membro:
            # Resetar usuário específico
            dados = self.get_user_data(ctx.guild.id, membro.id)
            dados['nivel'] = 1
            dados['xp'] = 0
            dados['mensagens'] = 0
            self.save_data()
            
            embed = discord.Embed(
                title="✅ Nível Resetado",
                description=f"O progresso de {membro.mention} foi resetado!",
                color=discord.Color.green()
            )
        else:
            # Confirmar reset do servidor
            embed_confirm = discord.Embed(
                title="⚠️ Confirmação Necessária",
                description="Tem certeza que deseja resetar **TODOS** os níveis do servidor?\n"
                           "Esta ação não pode ser desfeita!\n\n"
                           "Reaja com ✅ para confirmar ou ❌ para cancelar.",
                color=discord.Color.orange()
            )
            msg = await ctx.send(embed=embed_confirm)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id
            
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                
                if str(reaction.emoji) == "❌":
                    await ctx.send("❌ Reset cancelado.")
                    return
                
                # Resetar servidor
                guild_id = str(ctx.guild.id)
                self.data[guild_id] = {}
                self.save_data()
                
                embed = discord.Embed(
                    title="✅ Servidor Resetado",
                    description="Todos os níveis do servidor foram resetados!",
                    color=discord.Color.green()
                )
                
            except:
                await ctx.send("⏰ Tempo esgotado! Reset cancelado.")
                return
        
        await ctx.send(embed=embed)

    @app_commands.command(name='resetlevel', description='Reseta nível de um usuário ou do servidor (Administrador)')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(membro='Membro (opcional)')
    async def resetlevel_slash(self, interaction: discord.Interaction, membro: discord.Member = None):
        if membro:
            dados = self.get_user_data(interaction.guild.id, membro.id)
            dados['nivel'] = 1
            dados['xp'] = 0
            dados['mensagens'] = 0
            self.save_data()
            embed = discord.Embed(title="✅ Nível Resetado", description=f"O progresso de {membro.mention} foi resetado!", color=discord.Color.green())
            await interaction.response.send_message(embed=embed)
            return
        embed_confirm = discord.Embed(title="⚠️ Confirmação Necessária", description="Tem certeza que deseja resetar **TODOS** os níveis do servidor? Esta ação não pode ser desfeita!\nReaja com ✅ para confirmar ou ❌ para cancelar.", color=discord.Color.orange())
        msg = await interaction.channel.send(embed=embed_confirm)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            if str(reaction.emoji) == "❌":
                await interaction.channel.send("❌ Reset cancelado.")
                return
            guild_id = str(interaction.guild.id)
            self.data[guild_id] = {}
            self.save_data()
            embed = discord.Embed(title="✅ Servidor Resetado", description="Todos os níveis do servidor foram resetados!", color=discord.Color.green())
            await interaction.channel.send(embed=embed)
        except asyncio.TimeoutError:
            await interaction.channel.send("⏰ Tempo esgotado! Reset cancelado.")

async def setup(bot):
    await bot.add_cog(Niveis(bot))

