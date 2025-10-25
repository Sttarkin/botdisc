import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random
from datetime import datetime, timedelta

class Economia(commands.Cog):
    """Sistema de economia com moedas, trabalho e loja"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db_file = 'economia.json'
        self.load_data()
        
        with open('config.json', 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.loja_itens = {
            '🎮': {'nome': 'Console de Jogos', 'preco': 5000, 'descricao': 'Um console de última geração'},
            '🎸': {'nome': 'Guitarra', 'preco': 3000, 'descricao': 'Uma guitarra elétrica'},
            '🎨': {'nome': 'Kit de Pintura', 'preco': 1500, 'descricao': 'Kit completo para artistas'},
            '📚': {'nome': 'Coleção de Livros', 'preco': 2000, 'descricao': 'Coleção de livros raros'},
            '🏆': {'nome': 'Troféu de Ouro', 'preco': 10000, 'descricao': 'Troféu de campeão'},
            '💎': {'nome': 'Diamante', 'preco': 15000, 'descricao': 'Um diamante valioso'},
            '🚗': {'nome': 'Carro Esportivo', 'preco': 50000, 'descricao': 'Um carro de luxo'},
            '🏠': {'nome': 'Mansão', 'preco': 100000, 'descricao': 'Uma mansão gigante'}
        }
    
    def load_data(self):
        """Carrega os dados da economia"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {}
    
    def save_data(self):
        """Salva os dados da economia"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
    
    def get_user_data(self, user_id):
        """Obtém os dados de um usuário"""
        user_id = str(user_id)
        if user_id not in self.data:
            self.data[user_id] = {
                'coins': 0,
                'banco': 0,
                'inventario': [],
                'trabalho': None,
                'daily': None
            }
            self.save_data()
        return self.data[user_id]
    
    @commands.command(name='saldo', aliases=['bal', 'balance', 'dinheiro'])
    async def saldo(self, ctx, membro: discord.Member = None):
        """Mostra o saldo de um usuário"""
        membro = membro or ctx.author
        dados = self.get_user_data(membro.id)
        
        total = dados['coins'] + dados['banco']
        
        embed = discord.Embed(
            title=f"💰 Economia de {membro.display_name}",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=membro.display_avatar.url)
        embed.add_field(name="💵 Carteira", value=f"{dados['coins']} {self.config['moeda_nome']}", inline=True)
        embed.add_field(name="🏦 Banco", value=f"{dados['banco']} {self.config['moeda_nome']}", inline=True)
        embed.add_field(name="💎 Total", value=f"{total} {self.config['moeda_nome']}", inline=False)
        embed.timestamp = datetime.utcnow()
        
        await ctx.send(embed=embed)
    
    @commands.command(name='trabalhar', aliases=['work', 'trabalho'])
    @commands.cooldown(1, 3600, commands.BucketType.user)  # 1 hora
    async def trabalhar(self, ctx):
        """Trabalhe para ganhar moedas (cooldown: 1 hora)"""
        dados = self.get_user_data(ctx.author.id)
        
        # Trabalhos disponíveis
        trabalhos = [
            {'nome': 'Programador', 'min': 500, 'max': 1500},
            {'nome': 'Médico', 'min': 800, 'max': 2000},
            {'nome': 'Professor', 'min': 300, 'max': 800},
            {'nome': 'Engenheiro', 'min': 600, 'max': 1200},
            {'nome': 'Artista', 'min': 200, 'max': 1000},
            {'nome': 'Motorista', 'min': 250, 'max': 600},
            {'nome': 'Chef', 'min': 400, 'max': 900},
            {'nome': 'Streamer', 'min': 100, 'max': 2500}
        ]
        
        trabalho = random.choice(trabalhos)
        ganho = random.randint(trabalho['min'], trabalho['max'])
        
        dados['coins'] += ganho
        self.save_data()
        
        embed = discord.Embed(
            title="💼 Trabalho Concluído!",
            description=f"Você trabalhou como **{trabalho['nome']}** e ganhou **{ganho}** {self.config['moeda_emoji']}!",
            color=discord.Color.green()
        )
        embed.set_footer(text="Use !trabalhar novamente em 1 hora")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='daily', aliases=['diario'])
    async def daily(self, ctx):
        """Receba sua recompensa diária (cooldown: 24 horas)"""
        dados = self.get_user_data(ctx.author.id)
        
        # Verificar se já recebeu o daily hoje
        agora = datetime.utcnow()
        ultimo_daily = dados.get('daily')
        if ultimo_daily:
            ultimo_daily = datetime.fromisoformat(ultimo_daily)
            tempo_restante = timedelta(days=1) - (agora - ultimo_daily)
            
            if tempo_restante.total_seconds() > 0:
                horas = int(tempo_restante.total_seconds() // 3600)
                minutos = int((tempo_restante.total_seconds() % 3600) // 60)
                
                embed = discord.Embed(
                    title="⏰ Aguarde!",
                    description=f"Você já recebeu sua recompensa diária!\nVolte em **{horas}h {minutos}m**",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
        
        # Gerar recompensa
        ganho = random.randint(300, 800)
        bonus = random.randint(0, 500)
        total = ganho + bonus
        
        # Atualizar dados
        dados['coins'] += total
        dados['daily'] = agora.isoformat()
        self.save_data()
        
        # Enviar mensagem
        embed = discord.Embed(
            title="🎁 Recompensa Diária",
            description=f"Você recebeu sua recompensa diária!",
            color=discord.Color.blue()
        )
        embed.add_field(name="Base", value=f"{ganho} {self.config['moeda_emoji']}", inline=True)
        if bonus > 0:
            embed.add_field(name="🎉 Bônus", value=f"{bonus} {self.config['moeda_emoji']}", inline=True)
        embed.add_field(name="💰 Total", value=f"{total} {self.config['moeda_emoji']}", inline=False)
        embed.set_footer(text="Volte em 24 horas!")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='loja', aliases=['shop', 'store'])
    async def loja(self, ctx):
        """Mostra os itens disponíveis na loja"""
        embed = discord.Embed(
            title="🛒 Loja de Itens",
            description="Use `!comprar <emoji>` para comprar um item",
            color=discord.Color.blue()
        )
        
        for emoji, item in self.loja_itens.items():
            embed.add_field(
                name=f"{emoji} {item['nome']}",
                value=f"{item['descricao']}\n**Preço:** {item['preco']} {self.config['moeda_emoji']}",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='comprar', aliases=['buy'])
    async def comprar(self, ctx, item_emoji: str):
        """Compra um item da loja"""
        if item_emoji not in self.loja_itens:
            await ctx.send("❌ Item não encontrado! Use `!loja` para ver os itens disponíveis.")
            return
        
        dados = self.get_user_data(ctx.author.id)
        item = self.loja_itens[item_emoji]
        
        if dados['coins'] < item['preco']:
            falta = item['preco'] - dados['coins']
            await ctx.send(f"❌ Você não tem dinheiro suficiente! Faltam {falta} {self.config['moeda_emoji']}.")
            return
        
        # Verificar se já possui o item
        if item_emoji in dados['inventario']:
            await ctx.send("❌ Você já possui este item!")
            return
        
        # Realizar compra
        dados['coins'] -= item['preco']
        dados['inventario'].append(item_emoji)
        self.save_data()
        
        embed = discord.Embed(
            title="✅ Compra Realizada!",
            description=f"Você comprou **{item['nome']}** {item_emoji}!",
            color=discord.Color.green()
        )
        embed.add_field(name="Preço", value=f"{item['preco']} {self.config['moeda_emoji']}", inline=True)
        embed.add_field(name="Saldo Restante", value=f"{dados['coins']} {self.config['moeda_emoji']}", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='inventario', aliases=['inv', 'inventory'])
    async def inventario(self, ctx, membro: discord.Member = None):
        """Mostra o inventário de um usuário"""
        membro = membro or ctx.author
        dados = self.get_user_data(membro.id)
        
        embed = discord.Embed(
            title=f"🎒 Inventário de {membro.display_name}",
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=membro.display_avatar.url)
        
        if not dados['inventario']:
            embed.description = "Inventário vazio! Visite a loja para comprar itens."
        else:
            itens_str = ""
            valor_total = 0
            for emoji in dados['inventario']:
                if emoji in self.loja_itens:
                    item = self.loja_itens[emoji]
                    itens_str += f"{emoji} **{item['nome']}** - {item['preco']} {self.config['moeda_emoji']}\n"
                    valor_total += item['preco']
            
            embed.description = itens_str
            embed.add_field(
                name="💰 Valor Total",
                value=f"{valor_total} {self.config['moeda_emoji']}",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='dar', aliases=['give', 'doar'])
    async def dar(self, ctx, membro: discord.Member, quantidade: int):
        """Dá moedas para outro usuário"""
        if membro.bot:
            await ctx.send("❌ Você não pode dar moedas para bots!")
            return
        
        if membro.id == ctx.author.id:
            await ctx.send("❌ Você não pode dar moedas para si mesmo!")
            return
        
        if quantidade <= 0:
            await ctx.send("❌ A quantidade deve ser maior que zero!")
            return
        
        dados_autor = self.get_user_data(ctx.author.id)
        
        if dados_autor['coins'] < quantidade:
            await ctx.send(f"❌ Você não tem {quantidade} {self.config['moeda_emoji']} na carteira!")
            return
        
        dados_destino = self.get_user_data(membro.id)
        
        dados_autor['coins'] -= quantidade
        dados_destino['coins'] += quantidade
        self.save_data()
        
        embed = discord.Embed(
            title="💸 Transferência Realizada",
            description=f"{ctx.author.mention} deu **{quantidade}** {self.config['moeda_emoji']} para {membro.mention}!",
            color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='depositar', aliases=['dep', 'deposit'])
    async def depositar(self, ctx, quantidade: str):
        """Deposita moedas no banco"""
        dados = self.get_user_data(ctx.author.id)
        
        if quantidade.lower() == 'tudo' or quantidade.lower() == 'all':
            quantidade = dados['coins']
        else:
            try:
                quantidade = int(quantidade)
            except ValueError:
                await ctx.send("❌ Quantidade inválida!")
                return
        
        if quantidade <= 0:
            await ctx.send("❌ A quantidade deve ser maior que zero!")
            return
        
        if dados['coins'] < quantidade:
            await ctx.send(f"❌ Você não tem {quantidade} {self.config['moeda_emoji']} na carteira!")
            return
        
        dados['coins'] -= quantidade
        dados['banco'] += quantidade
        self.save_data()
        
        embed = discord.Embed(
            title="🏦 Depósito Realizado",
            description=f"Você depositou **{quantidade}** {self.config['moeda_emoji']} no banco!",
            color=discord.Color.green()
        )
        embed.add_field(name="Carteira", value=f"{dados['coins']} {self.config['moeda_emoji']}", inline=True)
        embed.add_field(name="Banco", value=f"{dados['banco']} {self.config['moeda_emoji']}", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='sacar', aliases=['withdraw', 'saque'])
    async def sacar(self, ctx, quantidade: str):
        """Saca moedas do banco"""
        dados = self.get_user_data(ctx.author.id)
        
        if quantidade.lower() == 'tudo' or quantidade.lower() == 'all':
            quantidade = dados['banco']
        else:
            try:
                quantidade = int(quantidade)
            except ValueError:
                await ctx.send("❌ Quantidade inválida!")
                return
        
        if quantidade <= 0:
            await ctx.send("❌ A quantidade deve ser maior que zero!")
            return
        
        if dados['banco'] < quantidade:
            await ctx.send(f"❌ Você não tem {quantidade} {self.config['moeda_emoji']} no banco!")
            return
        
        dados['banco'] -= quantidade
        dados['coins'] += quantidade
        self.save_data()
        
        embed = discord.Embed(
            title="💵 Saque Realizado",
            description=f"Você sacou **{quantidade}** {self.config['moeda_emoji']} do banco!",
            color=discord.Color.green()
        )
        embed.add_field(name="Carteira", value=f"{dados['coins']} {self.config['moeda_emoji']}", inline=True)
        embed.add_field(name="Banco", value=f"{dados['banco']} {self.config['moeda_emoji']}", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='apostar', aliases=['bet'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def apostar(self, ctx, quantidade: int):
        """Aposte suas moedas (50% de chance de ganhar o dobro)"""
        if quantidade <= 0:
            await ctx.send("❌ A quantidade deve ser maior que zero!")
            return
        
        dados = self.get_user_data(ctx.author.id)
        
        if dados['coins'] < quantidade:
            await ctx.send(f"❌ Você não tem {quantidade} {self.config['moeda_emoji']} na carteira!")
            return
        
        # 50% de chance
        ganhou = random.choice([True, False])
        
        if ganhou:
            ganho = quantidade
            dados['coins'] += ganho
            self.save_data()
            
            embed = discord.Embed(
                title="🎰 Você Ganhou!",
                description=f"Parabéns! Você ganhou **{ganho}** {self.config['moeda_emoji']}!",
                color=discord.Color.green()
            )
            embed.add_field(name="Novo Saldo", value=f"{dados['coins']} {self.config['moeda_emoji']}", inline=False)
        else:
            dados['coins'] -= quantidade
            self.save_data()
            
            embed = discord.Embed(
                title="😢 Você Perdeu!",
                description=f"Você perdeu **{quantidade}** {self.config['moeda_emoji']}...",
                color=discord.Color.red()
            )
            embed.add_field(name="Novo Saldo", value=f"{dados['coins']} {self.config['moeda_emoji']}", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='roubar', aliases=['rob', 'steal'])
    @commands.cooldown(1, 3600, commands.BucketType.user)  # 1 hora
    async def roubar(self, ctx, alvo: discord.Member):
        """Tente roubar moedas de outro usuário (cooldown: 1 hora)"""
        if alvo.bot:
            await ctx.send("❌ Você não pode roubar de bots!")
            return
        
        if alvo.id == ctx.author.id:
            await ctx.send("❌ Você não pode roubar de si mesmo!")
            return
        
        dados_ladrao = self.get_user_data(ctx.author.id)
        dados_alvo = self.get_user_data(alvo.id)
        
        if dados_alvo['coins'] < 100:
            await ctx.send(f"❌ {alvo.mention} não tem dinheiro suficiente para ser roubado!")
            return
        
        # 30% de chance de sucesso
        sucesso = random.randint(1, 100) <= 30
        
        if sucesso:
            # Roubar entre 10% e 30% do dinheiro do alvo
            porcentagem = random.randint(10, 30) / 100
            roubado = int(dados_alvo['coins'] * porcentagem)
            
            dados_alvo['coins'] -= roubado
            dados_ladrao['coins'] += roubado
            self.save_data()
            
            embed = discord.Embed(
                title="💰 Roubo Bem-Sucedido!",
                description=f"Você roubou **{roubado}** {self.config['moeda_emoji']} de {alvo.mention}!",
                color=discord.Color.green()
            )
        else:
            # Multa por falhar no roubo
            multa = min(dados_ladrao['coins'], 200)
            dados_ladrao['coins'] -= multa
            self.save_data()
            
            embed = discord.Embed(
                title="🚔 Roubo Fracassado!",
                description=f"Você foi pego tentando roubar e pagou uma multa de **{multa}** {self.config['moeda_emoji']}!",
                color=discord.Color.red()
            )
        
        await ctx.send(embed=embed)

    # --- Slash commands ---
    @app_commands.command(name='saldo', description='Mostra o saldo de um usuário')
    @app_commands.describe(membro='Membro (opcional)')
    async def saldo_slash(self, interaction: discord.Interaction, membro: discord.Member = None):
        membro = membro or interaction.user
        dados = self.get_user_data(membro.id)
        total = dados['coins'] + dados['banco']
        embed = discord.Embed(title=f"💰 Economia de {membro.display_name}", color=discord.Color.gold())
        embed.set_thumbnail(url=membro.display_avatar.url)
        embed.add_field(name="💵 Carteira", value=f"{dados['coins']} {self.config['moeda_nome']}", inline=True)
        embed.add_field(name="🏦 Banco", value=f"{dados['banco']} {self.config['moeda_nome']}", inline=True)
        embed.add_field(name="💎 Total", value=f"{total} {self.config['moeda_nome']}", inline=False)
        embed.timestamp = datetime.utcnow()
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='trabalhar', description='Trabalhe para ganhar moedas (cooldown aplicado por servidor)')
    async def trabalhar_slash(self, interaction: discord.Interaction):
        dados = self.get_user_data(interaction.user.id)
        trabalhos = [
            {'nome': 'Programador', 'min': 500, 'max': 1500},
            {'nome': 'Médico', 'min': 800, 'max': 2000},
            {'nome': 'Professor', 'min': 300, 'max': 800},
            {'nome': 'Engenheiro', 'min': 600, 'max': 1200},
            {'nome': 'Artista', 'min': 200, 'max': 1000},
            {'nome': 'Motorista', 'min': 250, 'max': 600},
            {'nome': 'Chef', 'min': 400, 'max': 900},
            {'nome': 'Streamer', 'min': 100, 'max': 2500}
        ]
        trabalho = random.choice(trabalhos)
        ganho = random.randint(trabalho['min'], trabalho['max'])
        dados['coins'] += ganho
        self.save_data()
        embed = discord.Embed(title="💼 Trabalho Concluído!", description=f"Você trabalhou como **{trabalho['nome']}** e ganhou **{ganho}** {self.config['moeda_emoji']}!", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='daily', description='Receba sua recompensa diária')
    async def daily_slash(self, interaction: discord.Interaction):
        dados = self.get_user_data(interaction.user.id)
        
        # Verificar se já recebeu o daily hoje
        agora = datetime.utcnow()
        ultimo_daily = dados.get('daily')
        if ultimo_daily:
            ultimo_daily = datetime.fromisoformat(ultimo_daily)
            tempo_restante = timedelta(days=1) - (agora - ultimo_daily)
            
            if tempo_restante.total_seconds() > 0:
                horas = int(tempo_restante.total_seconds() // 3600)
                minutos = int((tempo_restante.total_seconds() % 3600) // 60)
                
                embed = discord.Embed(
                    title="⏰ Aguarde!",
                    description=f"Você já recebeu sua recompensa diária!\nVolte em **{horas}h {minutos}m**",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        
        # Gerar recompensa
        ganho = random.randint(300, 800)
        bonus = random.randint(0, 500)
        total = ganho + bonus
        
        # Atualizar dados
        dados['coins'] += total
        dados['daily'] = agora.isoformat()
        self.save_data()
        
        # Enviar mensagem
        embed = discord.Embed(
            title="🎁 Recompensa Diária",
            description="Você recebeu sua recompensa diária!",
            color=discord.Color.blue()
        )
        embed.add_field(name="Base", value=f"{ganho} {self.config['moeda_emoji']}", inline=True)
        if bonus > 0:
            embed.add_field(name="🎉 Bônus", value=f"{bonus} {self.config['moeda_emoji']}", inline=True)
        embed.add_field(name="💰 Total", value=f"{total} {self.config['moeda_emoji']}", inline=False)
        embed.set_footer(text="Volte em 24 horas!")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='loja', description='Mostra os itens disponíveis na loja')
    async def loja_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🛒 Loja de Itens", description="Use `/comprar <emoji>` para comprar um item", color=discord.Color.blue())
        for emoji, item in self.loja_itens.items():
            embed.add_field(name=f"{emoji} {item['nome']}", value=f"{item['descricao']}\n**Preço:** {item['preco']} {self.config['moeda_emoji']}", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='comprar', description='Compra um item da loja')
    @app_commands.describe(item_emoji='Emoji do item')
    async def comprar_slash(self, interaction: discord.Interaction, item_emoji: str):
        if item_emoji not in self.loja_itens:
            await interaction.response.send_message("❌ Item não encontrado! Use `/loja` para ver os itens disponíveis.", ephemeral=True)
            return
        dados = self.get_user_data(interaction.user.id)
        item = self.loja_itens[item_emoji]
        if dados['coins'] < item['preco']:
            falta = item['preco'] - dados['coins']
            await interaction.response.send_message(f"❌ Você não tem dinheiro suficiente! Faltam {falta} {self.config['moeda_emoji']}.", ephemeral=True)
            return
        if item_emoji in dados['inventario']:
            await interaction.response.send_message("❌ Você já possui este item!", ephemeral=True)
            return
        dados['coins'] -= item['preco']
        dados['inventario'].append(item_emoji)
        self.save_data()
        embed = discord.Embed(title="✅ Compra Realizada!", description=f"Você comprou **{item['nome']}** {item_emoji}!", color=discord.Color.green())
        embed.add_field(name="Preço", value=f"{item['preco']} {self.config['moeda_emoji']}", inline=True)
        embed.add_field(name="Saldo Restante", value=f"{dados['coins']} {self.config['moeda_emoji']}", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='inventario', description='Mostra o inventário de um usuário')
    @app_commands.describe(membro='Membro (opcional)')
    async def inventario_slash(self, interaction: discord.Interaction, membro: discord.Member = None):
        membro = membro or interaction.user
        dados = self.get_user_data(membro.id)
        embed = discord.Embed(title=f"🎒 Inventário de {membro.display_name}", color=discord.Color.purple())
        embed.set_thumbnail(url=membro.display_avatar.url)
        if not dados['inventario']:
            embed.description = "Inventário vazio! Visite a loja para comprar itens."
        else:
            itens_str = ""
            valor_total = 0
            for emoji in dados['inventario']:
                if emoji in self.loja_itens:
                    item = self.loja_itens[emoji]
                    itens_str += f"{emoji} **{item['nome']}** - {item['preco']} {self.config['moeda_emoji']}\n"
                    valor_total += item['preco']
            embed.description = itens_str
            embed.add_field(name="💰 Valor Total", value=f"{valor_total} {self.config['moeda_emoji']}", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='dar', description='Dá moedas para outro usuário')
    @app_commands.describe(membro='Membro', quantidade='Quantidade')
    async def dar_slash(self, interaction: discord.Interaction, membro: discord.Member, quantidade: int):
        if membro.bot:
            await interaction.response.send_message("❌ Você não pode dar moedas para bots!", ephemeral=True)
            return
        if membro.id == interaction.user.id:
            await interaction.response.send_message("❌ Você não pode dar moedas para si mesmo!", ephemeral=True)
            return
        if quantidade <= 0:
            await interaction.response.send_message("❌ A quantidade deve ser maior que zero!", ephemeral=True)
            return
        dados_autor = self.get_user_data(interaction.user.id)
        if dados_autor['coins'] < quantidade:
            await interaction.response.send_message(f"❌ Você não tem {quantidade} {self.config['moeda_emoji']} na carteira!", ephemeral=True)
            return
        dados_destino = self.get_user_data(membro.id)
        dados_autor['coins'] -= quantidade
        dados_destino['coins'] += quantidade
        self.save_data()
        embed = discord.Embed(title="💸 Transferência Realizada", description=f"{interaction.user.mention} deu **{quantidade}** {self.config['moeda_emoji']} para {membro.mention}!", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='depositar', description='Deposita moedas no banco')
    @app_commands.describe(quantidade='Quantidade ou "tudo"')
    async def depositar_slash(self, interaction: discord.Interaction, quantidade: str):
        dados = self.get_user_data(interaction.user.id)
        if quantidade.lower() == 'tudo' or quantidade.lower() == 'all':
            quantidade_val = dados['coins']
        else:
            try:
                quantidade_val = int(quantidade)
            except ValueError:
                await interaction.response.send_message("❌ Quantidade inválida!", ephemeral=True)
                return
        if quantidade_val <= 0:
            await interaction.response.send_message("❌ A quantidade deve ser maior que zero!", ephemeral=True)
            return
        if dados['coins'] < quantidade_val:
            await interaction.response.send_message(f"❌ Você não tem {quantidade_val} {self.config['moeda_emoji']} na carteira!", ephemeral=True)
            return
        dados['coins'] -= quantidade_val
        dados['banco'] += quantidade_val
        self.save_data()
        embed = discord.Embed(title="🏦 Depósito Realizado", description=f"Você depositou **{quantidade_val}** {self.config['moeda_emoji']} no banco!", color=discord.Color.green())
        embed.add_field(name="Carteira", value=f"{dados['coins']} {self.config['moeda_emoji']}", inline=True)
        embed.add_field(name="Banco", value=f"{dados['banco']} {self.config['moeda_emoji']}", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='sacar', description='Saca moedas do banco')
    @app_commands.describe(quantidade='Quantidade ou "tudo"')
    async def sacar_slash(self, interaction: discord.Interaction, quantidade: str):
        dados = self.get_user_data(interaction.user.id)
        if quantidade.lower() == 'tudo' or quantidade.lower() == 'all':
            quantidade_val = dados['banco']
        else:
            try:
                quantidade_val = int(quantidade)
            except ValueError:
                await interaction.response.send_message("❌ Quantidade inválida!", ephemeral=True)
                return
        if quantidade_val <= 0:
            await interaction.response.send_message("❌ A quantidade deve ser maior que zero!", ephemeral=True)
            return
        if dados['banco'] < quantidade_val:
            await interaction.response.send_message(f"❌ Você não tem {quantidade_val} {self.config['moeda_emoji']} no banco!", ephemeral=True)
            return
        dados['banco'] -= quantidade_val
        dados['coins'] += quantidade_val
        self.save_data()
        embed = discord.Embed(title="💵 Saque Realizado", description=f"Você sacou **{quantidade_val}** {self.config['moeda_emoji']} do banco!", color=discord.Color.green())
        embed.add_field(name="Carteira", value=f"{dados['coins']} {self.config['moeda_emoji']}", inline=True)
        embed.add_field(name="Banco", value=f"{dados['banco']} {self.config['moeda_emoji']}", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='apostar', description='Aposte suas moedas (50% de chance de ganhar o dobro)')
    @app_commands.describe(quantidade='Quantidade a apostar')
    async def apostar_slash(self, interaction: discord.Interaction, quantidade: int):
        if quantidade <= 0:
            await interaction.response.send_message("❌ A quantidade deve ser maior que zero!", ephemeral=True)
            return
        dados = self.get_user_data(interaction.user.id)
        if dados['coins'] < quantidade:
            await interaction.response.send_message(f"❌ Você não tem {quantidade} {self.config['moeda_emoji']} na carteira!", ephemeral=True)
            return
        ganhou = random.choice([True, False])
        if ganhou:
            ganho = quantidade
            dados['coins'] += ganho
            self.save_data()
            embed = discord.Embed(title="🎰 Você Ganhou!", description=f"Parabéns! Você ganhou **{ganho}** {self.config['moeda_emoji']}!", color=discord.Color.green())
            embed.add_field(name="Novo Saldo", value=f"{dados['coins']} {self.config['moeda_emoji']}", inline=False)
        else:
            dados['coins'] -= quantidade
            self.save_data()
            embed = discord.Embed(title="😢 Você Perdeu!", description=f"Você perdeu **{quantidade}** {self.config['moeda_emoji']}...", color=discord.Color.red())
            embed.add_field(name="Novo Saldo", value=f"{dados['coins']} {self.config['moeda_emoji']}", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='roubar', description='Tente roubar moedas de outro usuário')
    @app_commands.describe(alvo='Membro alvo')
    async def roubar_slash(self, interaction: discord.Interaction, alvo: discord.Member):
        if alvo.bot:
            await interaction.response.send_message("❌ Você não pode roubar de bots!", ephemeral=True)
            return
        if alvo.id == interaction.user.id:
            await interaction.response.send_message("❌ Você não pode roubar de si mesmo!", ephemeral=True)
            return
        dados_ladrao = self.get_user_data(interaction.user.id)
        dados_alvo = self.get_user_data(alvo.id)
        if dados_alvo['coins'] < 100:
            await interaction.response.send_message(f"❌ {alvo.mention} não tem dinheiro suficiente para ser roubado!", ephemeral=True)
            return
        sucesso = random.randint(1, 100) <= 30
        if sucesso:
            porcentagem = random.randint(10, 30) / 100
            roubado = int(dados_alvo['coins'] * porcentagem)
            dados_alvo['coins'] -= roubado
            dados_ladrao['coins'] += roubado
            self.save_data()
            embed = discord.Embed(title="💰 Roubo Bem-Sucedido!", description=f"Você roubou **{roubado}** {self.config['moeda_emoji']} de {alvo.mention}!", color=discord.Color.green())
        else:
            multa = min(dados_ladrao['coins'], 200)
            dados_ladrao['coins'] -= multa
            self.save_data()
            embed = discord.Embed(title="🚔 Roubo Fracassado!", description=f"Você foi pego tentando roubar e pagou uma multa de **{multa}** {self.config['moeda_emoji']}!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Economia(bot))

