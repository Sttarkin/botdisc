import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import datetime

class Moderacao(commands.Cog):
    """Comandos de moderação do servidor"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='kick', aliases=['expulsar'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, motivo: str = "Não especificado"):
        """Expulsa um membro do servidor"""
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ Você não pode expulsar este membro!")
            return
        
        if member.id == ctx.author.id:
            await ctx.send("❌ Você não pode se expulsar!")
            return
        
        try:
            # Tentar enviar DM para o usuário
            try:
                embed_dm = discord.Embed(
                    title="👢 Você foi expulso!",
                    description=f"Servidor: **{ctx.guild.name}**\nMotivo: **{motivo}**",
                    color=discord.Color.orange()
                )
                await member.send(embed=embed_dm)
            except:
                pass
            
            # Expulsar
            await member.kick(reason=f"{ctx.author} - {motivo}")
            
            embed = discord.Embed(
                title="✅ Membro Expulso",
                color=discord.Color.green()
            )
            embed.add_field(name="Membro", value=member.mention, inline=True)
            embed.add_field(name="Moderador", value=ctx.author.mention, inline=True)
            embed.add_field(name="Motivo", value=motivo, inline=False)
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Erro ao expulsar: {e}")
    
    @commands.command(name='ban', aliases=['banir'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, motivo: str = "Não especificado"):
        """Bane um membro do servidor"""
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ Você não pode banir este membro!")
            return
        
        if member.id == ctx.author.id:
            await ctx.send("❌ Você não pode se banir!")
            return
        
        try:
            # Tentar enviar DM para o usuário
            try:
                embed_dm = discord.Embed(
                    title="🔨 Você foi banido!",
                    description=f"Servidor: **{ctx.guild.name}**\nMotivo: **{motivo}**",
                    color=discord.Color.red()
                )
                await member.send(embed=embed_dm)
            except:
                pass
            
            # Banir
            await member.ban(reason=f"{ctx.author} - {motivo}", delete_message_days=1)
            
            embed = discord.Embed(
                title="✅ Membro Banido",
                color=discord.Color.green()
            )
            embed.add_field(name="Membro", value=member.mention, inline=True)
            embed.add_field(name="Moderador", value=ctx.author.mention, inline=True)
            embed.add_field(name="Motivo", value=motivo, inline=False)
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Erro ao banir: {e}")
    
    @commands.command(name='unban', aliases=['desbanir'])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member_id: int):
        """Desbane um usuário pelo ID"""
        try:
            user = await self.bot.fetch_user(member_id)
            await ctx.guild.unban(user)
            
            embed = discord.Embed(
                title="✅ Usuário Desbanido",
                description=f"**{user.name}#{user.discriminator}** foi desbanido!",
                color=discord.Color.green()
            )
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            
        except discord.NotFound:
            await ctx.send("❌ Usuário não encontrado ou não está banido!")
        except Exception as e:
            await ctx.send(f"❌ Erro ao desbanir: {e}")
    
    @commands.command(name='clear', aliases=['limpar', 'purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, quantidade: int = 10):
        """Limpa mensagens do canal (máximo 100)"""
        if quantidade < 1 or quantidade > 100:
            await ctx.send("❌ Quantidade deve ser entre 1 e 100!")
            return
        
        try:
            deleted = await ctx.channel.purge(limit=quantidade + 1)  # +1 para incluir o comando
            
            embed = discord.Embed(
                title="🧹 Mensagens Limpas",
                description=f"**{len(deleted) - 1}** mensagens foram deletadas!",
                color=discord.Color.green()
            )
            
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(3)
            await msg.delete()
            
        except Exception as e:
            await ctx.send(f"❌ Erro ao limpar mensagens: {e}")
    
    @commands.command(name='mute', aliases=['mutar', 'silenciar'])
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, motivo: str = "Não especificado"):
        """Silencia um membro (remove permissão de enviar mensagens)"""
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ Você não pode silenciar este membro!")
            return
        
        # Procurar ou criar cargo "Mutado"
        mute_role = discord.utils.get(ctx.guild.roles, name="Mutado")
        
        if not mute_role:
            try:
                mute_role = await ctx.guild.create_role(
                    name="Mutado",
                    reason="Cargo necessário para o comando !mute"
                )
                
                # Atualizar permissões em todos os canais
                for channel in ctx.guild.channels:
                    await channel.set_permissions(mute_role, send_messages=False, speak=False)
                    
            except Exception as e:
                await ctx.send(f"❌ Erro ao criar cargo Mutado: {e}")
                return
        
        try:
            await member.add_roles(mute_role, reason=f"{ctx.author} - {motivo}")
            
            embed = discord.Embed(
                title="🔇 Membro Silenciado",
                color=discord.Color.orange()
            )
            embed.add_field(name="Membro", value=member.mention, inline=True)
            embed.add_field(name="Moderador", value=ctx.author.mention, inline=True)
            embed.add_field(name="Motivo", value=motivo, inline=False)
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Erro ao silenciar: {e}")
    
    @commands.command(name='unmute', aliases=['desmutar'])
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Remove o silenciamento de um membro"""
        mute_role = discord.utils.get(ctx.guild.roles, name="Mutado")
        
        if not mute_role:
            await ctx.send("❌ Cargo Mutado não existe!")
            return
        
        if mute_role not in member.roles:
            await ctx.send("❌ Este membro não está silenciado!")
            return
        
        try:
            await member.remove_roles(mute_role)
            
            embed = discord.Embed(
                title="🔊 Membro Dessilenciado",
                description=f"{member.mention} pode falar novamente!",
                color=discord.Color.green()
            )
            embed.timestamp = datetime.utcnow()
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Erro ao dessilenciar: {e}")
    
    @commands.command(name='warn', aliases=['avisar', 'advertir'])
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, motivo: str = "Não especificado"):
        """Avisa um membro"""
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ Você não pode avisar este membro!")
            return
        
        # Enviar DM para o usuário
        try:
            embed_dm = discord.Embed(
                title="⚠️ Você recebeu um aviso!",
                description=f"**Servidor:** {ctx.guild.name}\n**Motivo:** {motivo}",
                color=discord.Color.orange()
            )
            await member.send(embed=embed_dm)
        except:
            await ctx.send("⚠️ Não foi possível enviar DM para o usuário.")
        
        embed = discord.Embed(
            title="⚠️ Membro Avisado",
            color=discord.Color.orange()
        )
        embed.add_field(name="Membro", value=member.mention, inline=True)
        embed.add_field(name="Moderador", value=ctx.author.mention, inline=True)
        embed.add_field(name="Motivo", value=motivo, inline=False)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
    
    @commands.command(name='slowmode', aliases=['lento'])
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, segundos: int = 0):
        """Define o modo lento no canal (0 para desativar)"""
        if segundos < 0 or segundos > 21600:  # Máximo 6 horas
            await ctx.send("❌ O tempo deve ser entre 0 e 21600 segundos (6 horas)!")
            return
        
        try:
            await ctx.channel.edit(slowmode_delay=segundos)
            
            if segundos == 0:
                embed = discord.Embed(
                    title="✅ Modo Lento Desativado",
                    description="Membros podem enviar mensagens normalmente.",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="⏰ Modo Lento Ativado",
                    description=f"Intervalo de **{segundos}** segundos entre mensagens.",
                    color=discord.Color.orange()
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Erro ao definir modo lento: {e}")
    
    @commands.command(name='lock', aliases=['trancar'])
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        """Tranca o canal (membros não podem enviar mensagens)"""
        try:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            
            embed = discord.Embed(
                title="🔒 Canal Trancado",
                description="Membros não podem mais enviar mensagens neste canal.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Erro ao trancar canal: {e}")
    
    @commands.command(name='unlock', aliases=['destrancar'])
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        """Destranca o canal"""
        try:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
            
            embed = discord.Embed(
                title="🔓 Canal Destrancado",
                description="Membros podem enviar mensagens novamente.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Erro ao destrancar canal: {e}")

    # --- Slash command equivalents ---
    @app_commands.command(name='kick', description='Expulsa um membro do servidor')
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(member='Membro a ser expulso', motivo='Motivo da expulsão')
    async def kick_slash(self, interaction: discord.Interaction, member: discord.Member, motivo: str = "Não especificado"):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("❌ Você não pode expulsar este membro!", ephemeral=True)
            return
        if member.id == interaction.user.id:
            await interaction.response.send_message("❌ Você não pode se expulsar!", ephemeral=True)
            return
        try:
            try:
                embed_dm = discord.Embed(
                    title="👢 Você foi expulso!",
                    description=f"Servidor: **{interaction.guild.name}**\nMotivo: **{motivo}**",
                    color=discord.Color.orange()
                )
                await member.send(embed=embed_dm)
            except:
                pass
            await member.kick(reason=f"{interaction.user} - {motivo}")
            embed = discord.Embed(title="✅ Membro Expulso", color=discord.Color.green())
            embed.add_field(name="Membro", value=member.mention, inline=True)
            embed.add_field(name="Moderador", value=interaction.user.mention, inline=True)
            embed.add_field(name="Motivo", value=motivo, inline=False)
            embed.timestamp = datetime.utcnow()
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao expulsar: {e}", ephemeral=True)

    @app_commands.command(name='ban', description='Bane um membro do servidor')
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(member='Membro a ser banido', motivo='Motivo do ban')
    async def ban_slash(self, interaction: discord.Interaction, member: discord.Member, motivo: str = "Não especificado"):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("❌ Você não pode banir este membro!", ephemeral=True)
            return
        if member.id == interaction.user.id:
            await interaction.response.send_message("❌ Você não pode se banir!", ephemeral=True)
            return
        try:
            try:
                embed_dm = discord.Embed(
                    title="🔨 Você foi banido!",
                    description=f"Servidor: **{interaction.guild.name}**\nMotivo: **{motivo}**",
                    color=discord.Color.red()
                )
                await member.send(embed=embed_dm)
            except:
                pass
            await member.ban(reason=f"{interaction.user} - {motivo}", delete_message_days=1)
            embed = discord.Embed(title="✅ Membro Banido", color=discord.Color.green())
            embed.add_field(name="Membro", value=member.mention, inline=True)
            embed.add_field(name="Moderador", value=interaction.user.mention, inline=True)
            embed.add_field(name="Motivo", value=motivo, inline=False)
            embed.timestamp = datetime.utcnow()
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao banir: {e}", ephemeral=True)

    @app_commands.command(name='unban', description='Desbane um usuário pelo ID')
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(member_id='ID do usuário a desbanir')
    async def unban_slash(self, interaction: discord.Interaction, member_id: int):
        try:
            user = await self.bot.fetch_user(member_id)
            await interaction.guild.unban(user)
            embed = discord.Embed(title="✅ Usuário Desbanido", description=f"**{user.name}#{user.discriminator}** foi desbanido!", color=discord.Color.green())
            embed.timestamp = datetime.utcnow()
            await interaction.response.send_message(embed=embed)
        except discord.NotFound:
            await interaction.response.send_message("❌ Usuário não encontrado ou não está banido!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao desbanir: {e}", ephemeral=True)

    @app_commands.command(name='clear', description='Limpa mensagens do canal (máximo 100)')
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(quantidade='Quantidade de mensagens a remover (1-100)')
    async def clear_slash(self, interaction: discord.Interaction, quantidade: int = 10):
        if quantidade < 1 or quantidade > 100:
            await interaction.response.send_message("❌ Quantidade deve ser entre 1 e 100!", ephemeral=True)
            return
        try:
            await interaction.response.defer()
            deleted = await interaction.channel.purge(limit=quantidade)
            embed = discord.Embed(title="🧹 Mensagens Limpas", description=f"**{len(deleted)}** mensagens foram deletadas!", color=discord.Color.green())
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao limpar mensagens: {e}", ephemeral=True)

    @app_commands.command(name='mute', description='Silencia um membro')
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(member='Membro a ser silenciado', motivo='Motivo')
    async def mute_slash(self, interaction: discord.Interaction, member: discord.Member, motivo: str = "Não especificado"):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("❌ Você não pode silenciar este membro!", ephemeral=True)
            return
        mute_role = discord.utils.get(interaction.guild.roles, name="Mutado")
        if not mute_role:
            try:
                mute_role = await interaction.guild.create_role(name="Mutado", reason="Cargo necessário para o comando mute")
                for channel in interaction.guild.channels:
                    await channel.set_permissions(mute_role, send_messages=False, speak=False)
            except Exception as e:
                await interaction.response.send_message(f"❌ Erro ao criar cargo Mutado: {e}", ephemeral=True)
                return
        try:
            await member.add_roles(mute_role, reason=f"{interaction.user} - {motivo}")
            embed = discord.Embed(title="🔇 Membro Silenciado", color=discord.Color.orange())
            embed.add_field(name="Membro", value=member.mention, inline=True)
            embed.add_field(name="Moderador", value=interaction.user.mention, inline=True)
            embed.add_field(name="Motivo", value=motivo, inline=False)
            embed.timestamp = datetime.utcnow()
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao silenciar: {e}", ephemeral=True)

    @app_commands.command(name='unmute', description='Remove o silenciamento de um membro')
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.describe(member='Membro a dessilenciar')
    async def unmute_slash(self, interaction: discord.Interaction, member: discord.Member):
        mute_role = discord.utils.get(interaction.guild.roles, name="Mutado")
        if not mute_role:
            await interaction.response.send_message("❌ Cargo Mutado não existe!", ephemeral=True)
            return
        if mute_role not in member.roles:
            await interaction.response.send_message("❌ Este membro não está silenciado!", ephemeral=True)
            return
        try:
            await member.remove_roles(mute_role)
            embed = discord.Embed(title="🔊 Membro Dessilenciado", description=f"{member.mention} pode falar novamente!", color=discord.Color.green())
            embed.timestamp = datetime.utcnow()
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao dessilenciar: {e}", ephemeral=True)

    @app_commands.command(name='warn', description='Avisa um membro')
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(member='Membro a ser avisado', motivo='Motivo')
    async def warn_slash(self, interaction: discord.Interaction, member: discord.Member, motivo: str = "Não especificado"):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("❌ Você não pode avisar este membro!", ephemeral=True)
            return
        try:
            embed_dm = discord.Embed(title="⚠️ Você recebeu um aviso!", description=f"**Servidor:** {interaction.guild.name}\n**Motivo:** {motivo}", color=discord.Color.orange())
            await member.send(embed=embed_dm)
        except:
            pass
        embed = discord.Embed(title="⚠️ Membro Avisado", color=discord.Color.orange())
        embed.add_field(name="Membro", value=member.mention, inline=True)
        embed.add_field(name="Moderador", value=interaction.user.mention, inline=True)
        embed.add_field(name="Motivo", value=motivo, inline=False)
        embed.timestamp = datetime.utcnow()
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='slowmode', description='Define o modo lento no canal (0 para desativar)')
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.describe(segundos='Segundos de slowmode (0-21600)')
    async def slowmode_slash(self, interaction: discord.Interaction, segundos: int = 0):
        if segundos < 0 or segundos > 21600:
            await interaction.response.send_message("❌ O tempo deve ser entre 0 e 21600 segundos (6 horas)!", ephemeral=True)
            return
        try:
            await interaction.channel.edit(slowmode_delay=segundos)
            if segundos == 0:
                embed = discord.Embed(title="✅ Modo Lento Desativado", description="Membros podem enviar mensagens normalmente.", color=discord.Color.green())
            else:
                embed = discord.Embed(title="⏰ Modo Lento Ativado", description=f"Intervalo de **{segundos}** segundos entre mensagens.", color=discord.Color.orange())
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao definir modo lento: {e}", ephemeral=True)

    @app_commands.command(name='lock', description='Tranca o canal (membros não podem enviar mensagens)')
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock_slash(self, interaction: discord.Interaction):
        try:
            await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
            embed = discord.Embed(title="🔒 Canal Trancado", description="Membros não podem mais enviar mensagens neste canal.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao trancar canal: {e}", ephemeral=True)

    @app_commands.command(name='unlock', description='Destranca o canal')
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock_slash(self, interaction: discord.Interaction):
        try:
            await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
            embed = discord.Embed(title="🔓 Canal Destrancado", description="Membros podem enviar mensagens novamente.", color=discord.Color.green())
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erro ao destrancar canal: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderacao(bot))

