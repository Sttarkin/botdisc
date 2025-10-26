import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import json
import asyncio
import sys
from datetime import datetime
import os

class IA(commands.Cog):
    """Comandos relacionados à Inteligência Artificial"""
    
    def __init__(self, bot):
        self.bot = bot
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = "x-ai/grok-code-fast-1"
        self.conversations = {}  # Armazenar conversas por usuário
        self.log_channel_id = 1431654830572699730  # Canal de logs
        self.owner_id = 1386400784593326263  # ID do dono do bot
        
        # Carregar informações do bot
        self.bot_info = self.load_bot_info()
        
        # Prompt interno para definir personalidade e idioma
        self.system_prompt = {
            "role": "system",
            "content": self.create_system_prompt()
        }
    
    def load_bot_info(self):
        """Carregar informações do bot do arquivo JSON"""
        try:
            with open('bot_info.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("[AVISO] Arquivo bot_info.json não encontrado. Usando informações básicas.")
            return {
                "nome": "Bot Discord",
                "descricao": "Bot de Discord com IA",
                "funcionalidades": {},
                "comandos_especiais": {}
            }
        except Exception as e:
            print(f"[ERRO] Falha ao carregar bot_info.json: {e}")
            return {}
    
    def create_system_prompt(self):
        """Criar prompt do sistema com informações do bot"""
        base_prompt = """Você é Aziel, uma assistente de IA amigável e prestativa. Sempre responda em português brasileiro de forma clara e natural. Seja útil, educativa e mantenha um tom conversacional. Quando apropriado, use emojis para tornar as respostas mais amigáveis.

INFORMAÇÕES SOBRE O BOT:
- Nome: {nome}
- Descrição: {descricao}
- Prefixo: {prefixo}

COMANDOS PRINCIPAIS:
{comandos}

FUNCIONALIDADES:
{funcionalidades}

COMO AJUDAR USUÁRIOS:
- Use !ajuda para ver todos os comandos
- Use !ai para conversar comigo
- Use !info para informações do servidor
- Use !ping para verificar se o bot está online

Se alguém perguntar sobre sua identidade, diga que você é Aziel, a assistente de IA do servidor Discord. Se perguntarem sobre o bot, use as informações acima para ajudar."""

        # Construir lista de comandos
        comandos = []
        if "funcionalidades" in self.bot_info:
            for categoria, lista_comandos in self.bot_info["funcionalidades"].items():
                comandos.extend(lista_comandos)
        
        # Construir lista de funcionalidades
        funcionalidades = []
        if "funcionalidades" in self.bot_info:
            for categoria in self.bot_info["funcionalidades"].keys():
                funcionalidades.append(f"- {categoria.replace('_', ' ').title()}")
        
        return base_prompt.format(
            nome=self.bot_info.get("nome", "Bot Discord"),
            descricao=self.bot_info.get("descricao", "Bot de Discord com IA"),
            prefixo=self.bot_info.get("prefixo", "!"),
            comandos="\n".join(comandos[:20]),  # Limitar para não exceder tokens
            funcionalidades="\n".join(funcionalidades)
        )
    
    async def send_log(self, ctx, pergunta: str, resposta: str = None, erro: str = None):
        """Enviar log da interação com a IA para o canal de logs"""
        try:
            log_channel = self.bot.get_channel(self.log_channel_id)
            if not log_channel:
                print(f"[ERRO] Canal de logs não encontrado: {self.log_channel_id}")
                return
            
            # Criar embed de log
            embed = discord.Embed(
                title="📝 Log da Aziel",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            
            # Informações do usuário
            embed.add_field(
                name="👤 Usuário",
                value=f"{ctx.author.mention} ({ctx.author.id})",
                inline=True
            )
            
            # Servidor e canal
            embed.add_field(
                name="🏠 Servidor",
                value=f"{ctx.guild.name if ctx.guild else 'DM'}",
                inline=True
            )
            
            embed.add_field(
                name="📺 Canal",
                value=f"{ctx.channel.mention if ctx.channel else 'DM'}",
                inline=True
            )
            
            # Pergunta
            embed.add_field(
                name="❓ Pergunta",
                value=f"```{pergunta[:1000]}{'...' if len(pergunta) > 1000 else ''}```",
                inline=False
            )
            
            # Resposta ou erro
            if resposta:
                embed.add_field(
                    name="🤖 Resposta da Aziel",
                    value=f"```{resposta[:1000]}{'...' if len(resposta) > 1000 else ''}```",
                    inline=False
                )
                embed.color = discord.Color.green()
            elif erro:
                embed.add_field(
                    name="❌ Erro",
                    value=f"```{erro[:1000]}{'...' if len(erro) > 1000 else ''}```",
                    inline=False
                )
                embed.color = discord.Color.red()
            
            # Link para a mensagem original
            embed.add_field(
                name="🔗 Link Original",
                value=f"[Ir para mensagem]({ctx.message.jump_url})",
                inline=False
            )
            
            await log_channel.send(embed=embed)
            
        except Exception as e:
            print(f"[ERRO] Falha ao enviar log: {e}")

    async def send_log_interaction(self, interaction: discord.Interaction, pergunta: str = None, resposta: str = None, erro: str = None):
        """Enviar log usando uma Interaction (slash command)."""
        try:
            log_channel = self.bot.get_channel(self.log_channel_id)
            if not log_channel:
                print(f"[ERRO] Canal de logs não encontrado: {self.log_channel_id}")
                return
            embed = discord.Embed(title="📝 Log da Aziel", color=discord.Color.blue(), timestamp=datetime.utcnow())
            embed.add_field(name="👤 Usuário", value=f"{interaction.user.mention} ({interaction.user.id})", inline=True)
            embed.add_field(name="🏠 Servidor", value=f"{interaction.guild.name if interaction.guild else 'DM'}", inline=True)
            embed.add_field(name="📺 Canal", value=f"{interaction.channel.mention if interaction.channel else 'DM'}", inline=True)
            if pergunta:
                embed.add_field(name="❓ Pergunta", value=f"```{pergunta[:1000]}{'...' if len(pergunta) > 1000 else ''}```", inline=False)
            if resposta:
                embed.add_field(name="🤖 Resposta da Aziel", value=f"```{resposta[:1000]}{'...' if len(resposta) > 1000 else ''}```", inline=False)
                embed.color = discord.Color.green()
            if erro:
                embed.add_field(name="❌ Erro", value=f"```{erro[:1000]}{'...' if len(erro) > 1000 else ''}```", inline=False)
                embed.color = discord.Color.red()
            await log_channel.send(embed=embed)
        except Exception as e:
            print(f"[ERRO] Falha ao enviar log (interaction): {e}")
    
    @commands.command(name='ai', aliases=['aziel', 'chat'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ai_chat(self, ctx, *, pergunta: str = None):
        """Converse com a Aziel! Use !ai <sua pergunta>"""
        
        if not pergunta:
            embed = discord.Embed(
                title="🤖 Aziel - Assistente IA",
                description=f"**Como usar:** `{ctx.prefix}ai <sua pergunta>`\n\n"
                           "**Exemplos:**\n"
                           f"`{ctx.prefix}ai Como fazer um bot do Discord?`\n"
                           f"`{ctx.prefix}ai Explique Python para iniciantes`\n"
                           f"`{ctx.prefix}ai Qual a capital do Brasil?`\n\n"
                           f"**Aliases:** `{ctx.prefix}aziel`, `{ctx.prefix}chat`",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return
        
        # Verificar se a pergunta não é muito longa
        if len(pergunta) > 1000:
            embed = discord.Embed(
                title="❌ Pergunta muito longa",
                description="Sua pergunta deve ter no máximo 1000 caracteres.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Enviar mensagem de carregamento
        loading_embed = discord.Embed(
            title="🤖 Aziel pensando...",
            description="Aguarde um momento enquanto a Aziel processa sua pergunta...",
            color=discord.Color.yellow()
        )
        loading_msg = await ctx.send(embed=loading_embed)
        
        try:
            # Preparar mensagens para a API
            user_id = str(ctx.author.id)
            
            # Inicializar conversa se não existir
            if user_id not in self.conversations:
                self.conversations[user_id] = [self.system_prompt]  # Adicionar prompt do sistema
            
            # Adicionar pergunta do usuário
            self.conversations[user_id].append({
                "role": "user",
                "content": pergunta
            })
            
            # Manter apenas as últimas 10 mensagens + prompt do sistema para não exceder limites
            if len(self.conversations[user_id]) > 11:  # 1 prompt + 10 mensagens
                self.conversations[user_id] = [self.system_prompt] + self.conversations[user_id][-10:]
            
            # Fazer requisição para a API
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                payload = {
                    "model": self.model,
                    "messages": self.conversations[user_id],
                    "max_tokens": 1000,
                    "temperature": 0.7
                }
                
                async with session.post(self.api_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'choices' in data and len(data['choices']) > 0:
                            resposta = data['choices'][0]['message']['content']
                            
                            # Adicionar resposta da IA à conversa
                            self.conversations[user_id].append({
                                "role": "assistant",
                                "content": resposta
                            })
                            
                            # Enviar log da interação bem-sucedida
                            await self.send_log(ctx, pergunta, resposta)
                            
                            # Criar embed com a resposta
                            embed = discord.Embed(
                                title="🤖 Resposta da Aziel",
                                description=resposta[:4000],  # Limite do Discord
                                color=discord.Color.green(),
                                timestamp=datetime.utcnow()
                            )
                            embed.set_footer(text=f"Pergunta de {ctx.author.display_name}")
                            
                            # Se a resposta for muito longa, dividir em chunks
                            if len(resposta) > 4000:
                                chunks = [resposta[i:i+4000] for i in range(0, len(resposta), 4000)]
                                await loading_msg.delete()
                                
                                for i, chunk in enumerate(chunks):
                                    if i == 0:
                                        await ctx.send(embed=embed)
                                    else:
                                        await ctx.send(f"```\n{chunk}\n```")
                            else:
                                await loading_msg.edit(embed=embed)
                        else:
                            raise Exception("Resposta inválida da API")
                    else:
                        error_text = await response.text()
                        raise Exception(f"Erro da API: {response.status} - {error_text}")
        
        except asyncio.TimeoutError:
            error_msg = "Timeout - A Aziel demorou muito para responder"
            await self.send_log(ctx, pergunta, erro=error_msg)
            
            embed = discord.Embed(
                title="⏰ Timeout",
                description="A Aziel demorou muito para responder. Tente novamente.",
                color=discord.Color.red()
            )
            await loading_msg.edit(embed=embed)
        
        except Exception as e:
            error_msg = f"Erro: {str(e)}"
            await self.send_log(ctx, pergunta, erro=error_msg)
            
            embed = discord.Embed(
                title="❌ Erro",
                description=f"Ocorreu um erro ao processar sua pergunta:\n```{str(e)[:1000]}```",
                color=discord.Color.red()
            )
            await loading_msg.edit(embed=embed)
            print(f"Erro no comando IA: {e}")
    
    @commands.command(name='limpar_ia', aliases=['clear_ai', 'reset_ia'])
    async def limpar_conversa(self, ctx):
        """Limpa sua conversa com a Aziel"""
        user_id = str(ctx.author.id)
        
        # Log da ação
        await self.send_log(ctx, "COMANDO: limpar_ia", "Conversa limpa com sucesso")
        
        if user_id in self.conversations:
            del self.conversations[user_id]
            embed = discord.Embed(
                title="🧹 Conversa limpa",
                description="Sua conversa com a Aziel foi limpa com sucesso!",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="ℹ️ Nenhuma conversa",
                description="Você não tem nenhuma conversa ativa com a Aziel.",
                color=discord.Color.blue()
            )
        
        await ctx.send(embed=embed)

    @app_commands.command(name='ai', description='Converse com a Aziel (IA)')
    @app_commands.describe(pergunta='Sua pergunta para a Aziel')
    async def ai_slash(self, interaction: discord.Interaction, pergunta: str = None):
        if not pergunta:
            embed = discord.Embed(title="🤖 Aziel - Assistente IA", description="Use `/ai <sua pergunta>` para conversar com a Aziel.", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if len(pergunta) > 1000:
            embed = discord.Embed(title="❌ Pergunta muito longa", description="Sua pergunta deve ter no máximo 1000 caracteres.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await interaction.response.defer()
        try:
            user_id = str(interaction.user.id)
            if user_id not in self.conversations:
                self.conversations[user_id] = [self.system_prompt]
            self.conversations[user_id].append({"role": "user", "content": pergunta})
            if len(self.conversations[user_id]) > 11:
                self.conversations[user_id] = [self.system_prompt] + self.conversations[user_id][-10:]

            async with aiohttp.ClientSession() as session:
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
                payload = {"model": self.model, "messages": self.conversations[user_id], "max_tokens": 1000, "temperature": 0.7}
                async with session.post(self.api_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'choices' in data and len(data['choices']) > 0:
                            resposta = data['choices'][0]['message']['content']
                            self.conversations[user_id].append({"role": "assistant", "content": resposta})
                            await self.send_log_interaction(interaction, pergunta, resposta)
                            embed = discord.Embed(title="🤖 Resposta da Aziel", description=resposta[:4000], color=discord.Color.green(), timestamp=datetime.utcnow())
                            embed.set_footer(text=f"Pergunta de {interaction.user.display_name}")
                            await interaction.followup.send(embed=embed)
                        else:
                            raise Exception("Resposta inválida da API")
                    else:
                        error_text = await response.text()
                        raise Exception(f"Erro da API: {response.status} - {error_text}")
        except asyncio.TimeoutError:
            error_msg = "Timeout - A Aziel demorou muito para responder"
            await self.send_log_interaction(interaction, pergunta, erro=error_msg)
            embed = discord.Embed(title="⏰ Timeout", description="A Aziel demorou muito para responder. Tente novamente.", color=discord.Color.red())
            await interaction.followup.send(embed=embed)
        except Exception as e:
            error_msg = f"Erro: {str(e)}"
            await self.send_log_interaction(interaction, pergunta, erro=error_msg)
            embed = discord.Embed(title="❌ Erro", description=f"Ocorreu um erro ao processar sua pergunta:\n```{str(e)[:1000]}```", color=discord.Color.red())
            await interaction.followup.send(embed=embed)

    @app_commands.command(name='drop', description='Desliga o bot (apenas dono)')
    async def drop_slash(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            embed = discord.Embed(title="❌ Acesso Negado", description="Apenas o dono do bot pode usar este comando.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(title="💤 Desligando...", description="O bot está sendo desligado.", color=discord.Color.orange())
        await interaction.response.send_message(embed=embed)
        await self.send_log_interaction(interaction, "COMANDO: drop", "Bot desligado pelo dono")
        await self.bot.close()
        sys.exit(0)

    @app_commands.command(name='drop_database', description='Limpa o canal de logs')
    async def drop_database_slash(self, interaction: discord.Interaction):
        # Verificar se é o dono
        if interaction.user.id != self.owner_id:
            embed = discord.Embed(title="❌ Acesso Negado", description="Apenas o dono do bot pode usar este comando.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        log_channel = self.bot.get_channel(self.log_channel_id)
        if not log_channel:
            embed = discord.Embed(title="❌ Erro", description="Canal de logs não encontrado.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Deletar mensagem do comando
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Deletar mensagens do canal de log
            async for message in log_channel.history(limit=None):
                await message.delete()

            # Confirmar ação
            embed = discord.Embed(title="✅ Logs Limpos", description="O canal de logs foi limpo com sucesso.", color=discord.Color.green())
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            embed = discord.Embed(title="❌ Erro", description=f"Erro ao limpar logs: {str(e)}", color=discord.Color.red())
            await interaction.followup.send(embed=embed, ephemeral=True)    @app_commands.command(name='limpar_ia', description='Limpa sua conversa com a Aziel')
    async def limpar_conversa_slash(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        await self.send_log_interaction(interaction, "COMANDO: limpar_ia", "Conversa limpa com sucesso")
        if user_id in self.conversations:
            del self.conversations[user_id]
            embed = discord.Embed(title="🧹 Conversa limpa", description="Sua conversa com a Aziel foi limpa com sucesso!", color=discord.Color.green())
        else:
            embed = discord.Embed(title="ℹ️ Nenhuma conversa", description="Você não tem nenhuma conversa ativa com a Aziel.", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)
    
    @commands.command(name='status_ia')
    async def status_ia(self, ctx):
        """Mostra informações sobre a Aziel"""
        user_id = str(ctx.author.id)
        conversas_ativas = len(self.conversations)
        mensagens_usuario = len(self.conversations.get(user_id, []))
        
        embed = discord.Embed(
            title="🤖 Status da Aziel",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Nome",
            value="Aziel",
            inline=True
        )
        embed.add_field(
            name="Modelo",
            value="x-ai/grok-code-fast-1",
            inline=True
        )
        embed.add_field(
            name="Idioma",
            value="Português 🇧🇷",
            inline=True
        )
        embed.add_field(
            name="Conversas ativas",
            value=f"{conversas_ativas}",
            inline=True
        )
        embed.add_field(
            name="Suas mensagens",
            value=f"{mensagens_usuario}",
            inline=True
        )
        embed.add_field(
            name="Status",
            value="🟢 Online",
            inline=True
        )
        embed.add_field(
            name="Comandos disponíveis",
            value=f"`{ctx.prefix}ai` - Conversar com a Aziel\n"
                  f"`{ctx.prefix}aziel` - Alias para conversar\n"
                  f"`{ctx.prefix}limpar_ia` - Limpar conversa\n"
                  f"`{ctx.prefix}status_ia` - Ver status",
            inline=False
        )
        
        await ctx.send(embed=embed)

    @app_commands.command(name='status_ia', description='Mostra informações sobre a Aziel')
    async def status_ia_slash(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        conversas_ativas = len(self.conversations)
        mensagens_usuario = len(self.conversations.get(user_id, []))
        embed = discord.Embed(title="🤖 Status da Aziel", color=discord.Color.blue())
        embed.add_field(name="Nome", value="Aziel", inline=True)
        embed.add_field(name="Modelo", value=self.model, inline=True)
        embed.add_field(name="Idioma", value="Português 🇧🇷", inline=True)
        embed.add_field(name="Conversas ativas", value=f"{conversas_ativas}", inline=True)
        embed.add_field(name="Suas mensagens", value=f"{mensagens_usuario}", inline=True)
        embed.add_field(name="Status", value="🟢 Online", inline=True)
        embed.add_field(name="Comandos disponíveis", value="`/ai` - Conversar com a Aziel\n`/limpar_ia` - Limpar conversa\n`/status_ia` - Ver status", inline=False)
        await interaction.response.send_message(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Responder automaticamente a DMs"""
        # Ignorar mensagens do próprio bot
        if message.author == self.bot.user:
            return
        
        # Ignorar mensagens que começam com prefixo (comandos normais)
        if message.content.startswith(self.bot.command_prefix):
            return
        
        # Ignorar mensagens em servidores (apenas DMs)
        if message.guild is not None:
            return
        
        # Ignorar mensagens muito curtas ou vazias
        if len(message.content.strip()) < 3:
            return
        
        # Verificar se é um DM
        if isinstance(message.channel, discord.DMChannel):
            try:
                # Criar contexto falso para DM
                ctx = await self.bot.get_context(message)
                
                # Preparar mensagens para a API
                user_id = str(message.author.id)
                
                # Inicializar conversa se não existir
                if user_id not in self.conversations:
                    self.conversations[user_id] = [self.system_prompt]
                
                # Adicionar pergunta do usuário
                self.conversations[user_id].append({
                    "role": "user",
                    "content": message.content
                })
                
                # Manter apenas as últimas 10 mensagens + prompt do sistema
                if len(self.conversations[user_id]) > 11:
                    self.conversations[user_id] = [self.system_prompt] + self.conversations[user_id][-10:]
                
                # Fazer requisição para a API
                async with aiohttp.ClientSession() as session:
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"
                    }
                    
                    payload = {
                        "model": self.model,
                        "messages": self.conversations[user_id],
                        "max_tokens": 1000,
                        "temperature": 0.7
                    }
                    
                    async with session.post(self.api_url, headers=headers, json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            if 'choices' in data and len(data['choices']) > 0:
                                resposta = data['choices'][0]['message']['content']
                                
                                # Adicionar resposta da IA à conversa
                                self.conversations[user_id].append({
                                    "role": "assistant",
                                    "content": resposta
                                })
                                
                                # Enviar log da interação
                                await self.send_log(ctx, message.content, resposta)
                                
                                # Enviar resposta diretamente
                                await message.channel.send(resposta)
                            else:
                                await message.channel.send("❌ Desculpe, não consegui processar sua mensagem.")
                        else:
                            await message.channel.send("❌ Erro interno. Tente novamente mais tarde.")
                            
            except Exception as e:
                print(f"[ERRO] Falha ao responder DM: {e}")
                await message.channel.send("❌ Ocorreu um erro. Tente novamente mais tarde.")

async def setup(bot):
    await bot.add_cog(IA(bot))
