import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
from datetime import datetime

class Jogos(commands.Cog):
    """Mini jogos interativos"""
    
    def __init__(self, bot):
        self.bot = bot
        self.jogos_velha = {}
        
        self.quiz_perguntas = [
            {
                "pergunta": "Qual é a capital do Brasil?",
                "opcoes": ["São Paulo", "Brasília", "Rio de Janeiro", "Salvador"],
                "resposta": 1
            },
            {
                "pergunta": "Quantos planetas existem no Sistema Solar?",
                "opcoes": ["7", "8", "9", "10"],
                "resposta": 1
            },
            {
                "pergunta": "Qual é o maior oceano do mundo?",
                "opcoes": ["Atlântico", "Índico", "Pacífico", "Ártico"],
                "resposta": 2
            },
            {
                "pergunta": "Em que ano o Brasil foi descoberto?",
                "opcoes": ["1492", "1500", "1510", "1498"],
                "resposta": 1
            },
            {
                "pergunta": "Qual é o elemento químico com símbolo 'O'?",
                "opcoes": ["Ouro", "Ósmio", "Oxigênio", "Óxido"],
                "resposta": 2
            },
            {
                "pergunta": "Quantos continentes existem no mundo?",
                "opcoes": ["5", "6", "7", "8"],
                "resposta": 2
            },
            {
                "pergunta": "Qual é o animal terrestre mais rápido?",
                "opcoes": ["Leão", "Guepardo", "Leopardo", "Tigre"],
                "resposta": 1
            },
            {
                "pergunta": "Quantos dias tem um ano bissexto?",
                "opcoes": ["364", "365", "366", "367"],
                "resposta": 2
            }
        ]
    
    @commands.command(name='ppt', aliases=['pedrapapeltesoura', 'jokenpo'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pedra_papel_tesoura(self, ctx, escolha: str):
        """Jogue pedra, papel ou tesoura contra o bot"""
        escolha = escolha.lower()
        opcoes = ['pedra', 'papel', 'tesoura']
        
        if escolha not in opcoes:
            await ctx.send("❌ Escolha entre: pedra, papel ou tesoura!")
            return
        
        bot_escolha = random.choice(opcoes)
        
        # Emojis
        emojis = {
            'pedra': '🪨',
            'papel': '📄',
            'tesoura': '✂️'
        }
        
        # Determinar vencedor
        if escolha == bot_escolha:
            resultado = "Empate!"
            cor = discord.Color.gold()
        elif (escolha == 'pedra' and bot_escolha == 'tesoura') or \
             (escolha == 'papel' and bot_escolha == 'pedra') or \
             (escolha == 'tesoura' and bot_escolha == 'papel'):
            resultado = "🎉 Você venceu!"
            cor = discord.Color.green()
        else:
            resultado = "😢 Você perdeu!"
            cor = discord.Color.red()
        
        embed = discord.Embed(
            title="🎮 Pedra, Papel ou Tesoura",
            color=cor
        )
        embed.add_field(
            name="Sua escolha",
            value=f"{emojis[escolha]} {escolha.capitalize()}",
            inline=True
        )
        embed.add_field(
            name="Minha escolha",
            value=f"{emojis[bot_escolha]} {bot_escolha.capitalize()}",
            inline=True
        )
        embed.add_field(name="Resultado", value=resultado, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='adivinhar', aliases=['guess', 'adivinha'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def adivinhar(self, ctx):
        """Tente adivinhar o número que o bot está pensando (1-100)"""
        numero = random.randint(1, 100)
        tentativas = 0
        max_tentativas = 7
        
        embed = discord.Embed(
            title="🎯 Jogo de Adivinhação",
            description=f"Estou pensando em um número entre **1** e **100**!\n"
                       f"Você tem **{max_tentativas}** tentativas.\n"
                       f"Digite um número para começar!",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
        
        while tentativas < max_tentativas:
            try:
                msg = await self.bot.wait_for('message', timeout=30.0, check=check)
                tentativas += 1
                palpite = int(msg.content)
                
                if palpite < 1 or palpite > 100:
                    await ctx.send("❌ Número deve estar entre 1 e 100!")
                    tentativas -= 1
                    continue
                
                if palpite == numero:
                    embed = discord.Embed(
                        title="🎉 Parabéns!",
                        description=f"Você acertou! O número era **{numero}**!\n"
                                   f"Tentativas: **{tentativas}**/{max_tentativas}",
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                    return
                
                elif palpite < numero:
                    dica = "📈 O número é **maior**!"
                else:
                    dica = "📉 O número é **menor**!"
                
                restantes = max_tentativas - tentativas
                await ctx.send(f"{dica} Tentativas restantes: **{restantes}**")
                
            except asyncio.TimeoutError:
                await ctx.send("⏰ Tempo esgotado! Jogo cancelado.")
                return
        
        embed = discord.Embed(
            title="😢 Game Over",
            description=f"Suas tentativas acabaram!\nO número era **{numero}**.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='quiz', aliases=['trivia'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def quiz(self, ctx):
        """Responda perguntas de um quiz"""
        pergunta = random.choice(self.quiz_perguntas)
        
        # Criar embed com a pergunta
        embed = discord.Embed(
            title="🧠 Quiz",
            description=f"**{pergunta['pergunta']}**",
            color=discord.Color.blue()
        )
        
        for i, opcao in enumerate(pergunta['opcoes'], 1):
            embed.add_field(name=f"Opção {i}", value=opcao, inline=False)
        
        embed.set_footer(text="Você tem 15 segundos para responder! Digite o número da resposta (1-4)")
        
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content in ['1', '2', '3', '4']
        
        try:
            msg = await self.bot.wait_for('message', timeout=15.0, check=check)
            resposta_usuario = int(msg.content) - 1
            
            if resposta_usuario == pergunta['resposta']:
                embed = discord.Embed(
                    title="✅ Correto!",
                    description=f"Parabéns! A resposta correta é: **{pergunta['opcoes'][pergunta['resposta']]}**",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="❌ Incorreto!",
                    description=f"A resposta correta era: **{pergunta['opcoes'][pergunta['resposta']]}**",
                    color=discord.Color.red()
                )
            
            await ctx.send(embed=embed)
            
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="⏰ Tempo Esgotado!",
                description=f"A resposta correta era: **{pergunta['opcoes'][pergunta['resposta']]}**",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
    
    @commands.command(name='velha', aliases=['tictactoe', 'jogodavelha'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def jogo_da_velha(self, ctx, oponente: discord.Member):
        """Jogue jogo da velha contra outro usuário"""
        if oponente.bot:
            await ctx.send("❌ Você não pode jogar contra um bot!")
            return
        
        if oponente.id == ctx.author.id:
            await ctx.send("❌ Você não pode jogar contra si mesmo!")
            return
        
        if ctx.author.id in self.jogos_velha:
            await ctx.send("❌ Você já está em um jogo!")
            return
        
        # Pedir confirmação do oponente
        embed = discord.Embed(
            title="⭕ Jogo da Velha",
            description=f"{oponente.mention}, {ctx.author.mention} desafia você para um jogo da velha!\n"
                       f"Reaja com ✅ para aceitar ou ❌ para recusar.",
            color=discord.Color.blue()
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        
        def check_reaction(reaction, user):
            return user == oponente and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check_reaction)
            
            if str(reaction.emoji) == "❌":
                await ctx.send(f"😢 {oponente.mention} recusou o desafio!")
                return
            
        except asyncio.TimeoutError:
            await ctx.send("⏰ O desafio expirou!")
            return
        
        # Iniciar jogo
        jogo = {
            'tabuleiro': [[' ' for _ in range(3)] for _ in range(3)],
            'jogador1': ctx.author,
            'jogador2': oponente,
            'atual': ctx.author,
            'simbolo1': '❌',
            'simbolo2': '⭕'
        }
        
        self.jogos_velha[ctx.author.id] = jogo
        self.jogos_velha[oponente.id] = jogo
        
        await self.mostrar_tabuleiro(ctx, jogo)
    
    async def mostrar_tabuleiro(self, ctx, jogo):
        """Mostra o tabuleiro do jogo da velha.
        Aceita tanto um `ctx` tradicional quanto um `discord.Interaction`.
        """
        is_interaction = isinstance(ctx, discord.Interaction)

        # Preparar canal e função de envio compatível
        if is_interaction:
            channel = ctx.channel
            author = ctx.user
            async def send_func(*args, **kwargs):
                return await channel.send(*args, **kwargs)
        else:
            channel = ctx.channel
            author = ctx.author
            send_func = ctx.send

        def build_tab():
            tabuleiro_str = ""
            for i, linha in enumerate(jogo['tabuleiro']):
                tabuleiro_str += " | ".join(linha) + "\n"
                if i < 2:
                    tabuleiro_str += "―" * 9 + "\n"
            return tabuleiro_str

        tabuleiro_str = build_tab()
        simbolo = jogo['simbolo1'] if jogo['atual'] == jogo['jogador1'] else jogo['simbolo2']

        embed = discord.Embed(
            title="⭕ Jogo da Velha",
            description=f"```\n{tabuleiro_str}\n```",
            color=discord.Color.blue()
        )
        embed.add_field(name="Jogadores", value=f"{jogo['simbolo1']} {jogo['jogador1'].mention}\n{jogo['simbolo2']} {jogo['jogador2'].mention}", inline=True)
        embed.add_field(name="Vez de", value=f"{simbolo} {jogo['atual'].mention}", inline=True)
        embed.set_footer(text="Digite a posição (1-9) para jogar:\n1 2 3\n4 5 6\n7 8 9")

        msg = await send_func(embed=embed)

        # Aguardar jogada
        def check(m):
            return m.author == jogo['atual'] and m.channel == channel and m.content.isdigit()

        try:
            msg_in = await self.bot.wait_for('message', timeout=60.0, check=check)
            posicao = int(msg_in.content)

            if posicao < 1 or posicao > 9:
                await send_func("❌ Posição inválida! Use números de 1 a 9.")
                return await self.mostrar_tabuleiro(ctx, jogo)

            linha = (posicao - 1) // 3
            coluna = (posicao - 1) % 3

            if jogo['tabuleiro'][linha][coluna] != ' ':
                await send_func("❌ Essa posição já está ocupada!")
                return await self.mostrar_tabuleiro(ctx, jogo)

            simbolo = jogo['simbolo1'] if jogo['atual'] == jogo['jogador1'] else jogo['simbolo2']
            jogo['tabuleiro'][linha][coluna] = simbolo

            # Verificar vitória
            if self.verificar_vitoria(jogo['tabuleiro'], simbolo):
                tabuleiro_str = build_tab()
                embed = discord.Embed(title="🎉 Vitória!", description=f"```\n{tabuleiro_str}\n```\n{jogo['atual'].mention} venceu!", color=discord.Color.green())
                await send_func(embed=embed)
                del self.jogos_velha[jogo['jogador1'].id]
                del self.jogos_velha[jogo['jogador2'].id]
                return

            # Verificar empate
            if all(jogo['tabuleiro'][i][j] != ' ' for i in range(3) for j in range(3)):
                tabuleiro_str = build_tab()
                embed = discord.Embed(title="🤝 Empate!", description=f"```\n{tabuleiro_str}\n```\nO jogo empatou!", color=discord.Color.gold())
                await send_func(embed=embed)
                del self.jogos_velha[jogo['jogador1'].id]
                del self.jogos_velha[jogo['jogador2'].id]
                return

            # Trocar jogador
            jogo['atual'] = jogo['jogador2'] if jogo['atual'] == jogo['jogador1'] else jogo['jogador1']
            await self.mostrar_tabuleiro(ctx, jogo)

        except asyncio.TimeoutError:
            await send_func("⏰ Tempo esgotado! Jogo cancelado.")
            if jogo['jogador1'].id in self.jogos_velha:
                del self.jogos_velha[jogo['jogador1'].id]
            if jogo['jogador2'].id in self.jogos_velha:
                del self.jogos_velha[jogo['jogador2'].id]
    
    def verificar_vitoria(self, tabuleiro, simbolo):
        """Verifica se há vitória no jogo da velha"""
        # Verificar linhas
        for linha in tabuleiro:
            if all(cell == simbolo for cell in linha):
                return True
        
        # Verificar colunas
        for col in range(3):
            if all(tabuleiro[row][col] == simbolo for row in range(3)):
                return True
        
        # Verificar diagonais
        if all(tabuleiro[i][i] == simbolo for i in range(3)):
            return True
        if all(tabuleiro[i][2-i] == simbolo for i in range(3)):
            return True
        
        return False
    
    @commands.command(name='coinrace', aliases=['corrida_moedas'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def coinrace(self, ctx):
        """Jogue uma corrida de moedas!"""
        jogadores = ['🔴', '🔵', '🟢', '🟡']
        posicoes = [0, 0, 0, 0]
        meta = 10
        
        embed = discord.Embed(
            title="🏁 Corrida de Moedas",
            description="A corrida começou!",
            color=discord.Color.blue()
        )
        
        msg = await ctx.send(embed=embed)
        
        vencedor = None
        while vencedor is None:
            await asyncio.sleep(1)
            
            # Mover jogadores aleatoriamente
            for i in range(len(jogadores)):
                posicoes[i] += random.randint(1, 3)
                if posicoes[i] >= meta:
                    vencedor = i
                    posicoes[i] = meta
            
            # Criar visual da corrida
            corrida = ""
            for i, jogador in enumerate(jogadores):
                pista = "▬" * posicoes[i] + jogador + "▬" * (meta - posicoes[i])
                corrida += f"{pista} | {posicoes[i]}/{meta}\n"
            
            embed.description = f"```\n{corrida}\n```"
            await msg.edit(embed=embed)
            
            if vencedor is not None:
                break
        
        embed.title = "🏆 Corrida Finalizada!"
        embed.description = f"```\n{corrida}\n```\n🎉 O vencedor é {jogadores[vencedor]}!"
        embed.color = discord.Color.green()
        
        await msg.edit(embed=embed)

    # --- Slash command equivalents ---
    @app_commands.command(name='ppt', description='Jogue pedra, papel ou tesoura contra o bot')
    @app_commands.describe(escolha='pedra, papel ou tesoura')
    async def ppt_slash(self, interaction: discord.Interaction, escolha: str):
        escolha = escolha.lower()
        opcoes = ['pedra', 'papel', 'tesoura']
        if escolha not in opcoes:
            await interaction.response.send_message("❌ Escolha entre: pedra, papel ou tesoura!", ephemeral=True)
            return
        bot_escolha = random.choice(opcoes)
        emojis = {'pedra': '🪨', 'papel': '📄', 'tesoura': '✂️'}
        if escolha == bot_escolha:
            resultado = "Empate!"; cor = discord.Color.gold()
        elif (escolha == 'pedra' and bot_escolha == 'tesoura') or (escolha == 'papel' and bot_escolha == 'pedra') or (escolha == 'tesoura' and bot_escolha == 'papel'):
            resultado = "🎉 Você venceu!"; cor = discord.Color.green()
        else:
            resultado = "😢 Você perdeu!"; cor = discord.Color.red()
        embed = discord.Embed(title="🎮 Pedra, Papel ou Tesoura", color=cor)
        embed.add_field(name="Sua escolha", value=f"{emojis[escolha]} {escolha.capitalize()}", inline=True)
        embed.add_field(name="Minha escolha", value=f"{emojis[bot_escolha]} {bot_escolha.capitalize()}", inline=True)
        embed.add_field(name="Resultado", value=resultado, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='adivinhar', description='Tente adivinhar o número que o bot está pensando (1-100)')
    async def adivinhar_slash(self, interaction: discord.Interaction):
        numero = random.randint(1, 100)
        tentativas = 0
        max_tentativas = 7
        await interaction.response.send_message(embed=discord.Embed(title="🎯 Jogo de Adivinhação", description=f"Estou pensando em um número entre **1** e **100**! Você tem **{max_tentativas}** tentativas. Digite um número para começar!", color=discord.Color.blue()))

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit()

        while tentativas < max_tentativas:
            try:
                msg = await self.bot.wait_for('message', timeout=30.0, check=check)
                tentativas += 1
                palpite = int(msg.content)
                if palpite < 1 or palpite > 100:
                    await interaction.channel.send("❌ Número deve estar entre 1 e 100!")
                    tentativas -= 1
                    continue
                if palpite == numero:
                    embed = discord.Embed(title="🎉 Parabéns!", description=f"Você acertou! O número era **{numero}**!\nTentativas: **{tentativas}**/{max_tentativas}", color=discord.Color.green())
                    await interaction.channel.send(embed=embed)
                    return
                elif palpite < numero:
                    dica = "📈 O número é **maior**!"
                else:
                    dica = "📉 O número é **menor**!"
                restantes = max_tentativas - tentativas
                await interaction.channel.send(f"{dica} Tentativas restantes: **{restantes}**")
            except asyncio.TimeoutError:
                await interaction.channel.send("⏰ Tempo esgotado! Jogo cancelado.")
                return
        embed = discord.Embed(title="😢 Game Over", description=f"Suas tentativas acabaram! O número era **{numero}**.", color=discord.Color.red())
        await interaction.channel.send(embed=embed)

    @app_commands.command(name='quiz', description='Responda perguntas de um quiz')
    async def quiz_slash(self, interaction: discord.Interaction):
        pergunta = random.choice(self.quiz_perguntas)
        embed = discord.Embed(title="🧠 Quiz", description=f"**{pergunta['pergunta']}**", color=discord.Color.blue())
        for i, opcao in enumerate(pergunta['opcoes'], 1):
            embed.add_field(name=f"Opção {i}", value=opcao, inline=False)
        embed.set_footer(text="Você tem 15 segundos para responder! Digite o número da resposta (1-4)")
        await interaction.response.send_message(embed=embed)
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel and m.content in ['1','2','3','4']
        try:
            msg = await self.bot.wait_for('message', timeout=15.0, check=check)
            resposta_usuario = int(msg.content) - 1
            if resposta_usuario == pergunta['resposta']:
                embed = discord.Embed(title="✅ Correto!", description=f"Parabéns! A resposta correta é: **{pergunta['opcoes'][pergunta['resposta']]}**", color=discord.Color.green())
            else:
                embed = discord.Embed(title="❌ Incorreto!", description=f"A resposta correta era: **{pergunta['opcoes'][pergunta['resposta']]}**", color=discord.Color.red())
            await interaction.channel.send(embed=embed)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="⏰ Tempo Esgotado!", description=f"A resposta correta era: **{pergunta['opcoes'][pergunta['resposta']]}**", color=discord.Color.orange())
            await interaction.channel.send(embed=embed)

    @app_commands.command(name='velha', description='Jogue jogo da velha contra outro usuário')
    @app_commands.describe(oponente='Oponente do jogo')
    async def velha_slash(self, interaction: discord.Interaction, oponente: discord.Member):
        if oponente.bot:
            await interaction.response.send_message("❌ Você não pode jogar contra um bot!", ephemeral=True)
            return
        if oponente.id == interaction.user.id:
            await interaction.response.send_message("❌ Você não pode jogar contra si mesmo!", ephemeral=True)
            return
        if interaction.user.id in self.jogos_velha:
            await interaction.response.send_message("❌ Você já está em um jogo!", ephemeral=True)
            return
        embed = discord.Embed(title="⭕ Jogo da Velha", description=f"{oponente.mention}, {interaction.user.mention} desafia você para um jogo da velha! Reaja com ✅ para aceitar ou ❌ para recusar.", color=discord.Color.blue())
        msg = await interaction.channel.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        def check_reaction(reaction, user):
            return user == oponente and str(reaction.emoji) in ["✅","❌"] and reaction.message.id == msg.id
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check_reaction)
            if str(reaction.emoji) == "❌":
                await interaction.channel.send(f"😢 {oponente.mention} recusou o desafio!")
                return
        except asyncio.TimeoutError:
            await interaction.channel.send("⏰ O desafio expirou!")
            return
        jogo = {'tabuleiro': [[' ' for _ in range(3)] for _ in range(3)], 'jogador1': interaction.user, 'jogador2': oponente, 'atual': interaction.user, 'simbolo1':'❌','simbolo2':'⭕'}
        self.jogos_velha[interaction.user.id] = jogo
        self.jogos_velha[oponente.id] = jogo
        # Reusar mostrar_tabuleiro (precisa adaptar para aceitar interaction)
        await self.mostrar_tabuleiro(interaction, jogo)

    @app_commands.command(name='coinrace', description='Jogue uma corrida de moedas')
    async def coinrace_slash(self, interaction: discord.Interaction):
        jogadores = ['🔴', '🔵', '🟢', '🟡']
        posicoes = [0, 0, 0, 0]
        meta = 10
        embed = discord.Embed(title="🏁 Corrida de Moedas", description="A corrida começou!", color=discord.Color.blue())
        msg = await interaction.channel.send(embed=embed)
        vencedor = None
        while vencedor is None:
            await asyncio.sleep(1)
            for i in range(len(jogadores)):
                posicoes[i] += random.randint(1, 3)
                if posicoes[i] >= meta:
                    vencedor = i
                    posicoes[i] = meta
            corrida = ""
            for i, jogador in enumerate(jogadores):
                pista = "▬" * posicoes[i] + jogador + "▬" * (meta - posicoes[i])
                corrida += f"{pista} | {posicoes[i]}/{meta}\n"
            embed.description = f"```\n{corrida}\n```"
            await msg.edit(embed=embed)
            if vencedor is not None:
                break
        embed.title = "🏆 Corrida Finalizada!"
        embed.description = f"```\n{corrida}\n```\n🎉 O vencedor é {jogadores[vencedor]}!"
        embed.color = discord.Color.green()
        await msg.edit(embed=embed)

async def setup(bot):
    await bot.add_cog(Jogos(bot))

