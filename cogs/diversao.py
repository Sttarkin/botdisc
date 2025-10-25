import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
from datetime import datetime
import aiohttp

class Diversao(commands.Cog):
    """Comandos de diversão e entretenimento"""
    
    def __init__(self, bot):
        self.bot = bot
        
        self.piadas = [
            "Por que o livro de matemática se suicidou? Porque tinha muitos problemas! 😅",
            "O que o pato disse para a pata? Vem quá! 🦆",
            "Por que o Batman colocou o Bat-móvel no seguro? Por causa do Robin! 🦇",
            "O que é um pontinho amarelo no meio do mar? Ruffles, a batata da onda! 🌊",
            "Por que a galinha atravessou a rua? Para chegar do outro lado! 🐔",
            "O que o tomate foi fazer no banco? Tirar extrato! 🍅",
            "Como se chama um gato que caiu na lama? Gatolama! 🐱",
            "O que é um pontinho verde brilhando na cama? Uma ervilha que ainda não apagou a luz! 💡",
            "Por que o elefante não pega fogo? Porque ele já é cinza! 🐘",
            "O que a esfera disse para o cubo? Deixa de ser quadrado! ⚽"
        ]
        
        self.fatos = [
            "🌍 A Lua está se afastando da Terra cerca de 3,8 cm por ano.",
            "🐙 Os polvos têm três corações!",
            "🍯 O mel nunca estraga. Arqueólogos encontraram mel de 3000 anos ainda comestível!",
            "🦒 As girafas têm a mesma quantidade de ossos no pescoço que os humanos: 7!",
            "🌟 Existem mais estrelas no universo do que grãos de areia em todas as praias da Terra.",
            "🐌 Os caracóis podem dormir por até 3 anos!",
            "⚡ Um raio é cinco vezes mais quente que a superfície do Sol.",
            "🦈 Tubarões são mais antigos que árvores!",
            "🧠 O cérebro humano usa 20% da energia do corpo, apesar de representar apenas 2% do peso.",
            "🐝 As abelhas conseguem reconhecer rostos humanos!"
        ]
    
    @commands.command(name='dado', aliases=['roll', 'rolar'])
    async def dado(self, ctx, lados: int = 6):
        """Rola um dado (padrão: 6 lados)"""
        if lados < 2 or lados > 100:
            await ctx.send("❌ O dado deve ter entre 2 e 100 lados!")
            return
        
        resultado = random.randint(1, lados)
        
        embed = discord.Embed(
            title="🎲 Rolando o Dado...",
            description=f"**Resultado:** {resultado}",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Dado de {lados} lados")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='moeda', aliases=['coinflip', 'cara_coroa'])
    async def moeda(self, ctx):
        """Joga uma moeda (cara ou coroa)"""
        resultado = random.choice(['Cara', 'Coroa'])
        emoji = '🪙' if resultado == 'Cara' else '💿'
        
        msg = await ctx.send("🪙 Jogando a moeda...")
        await asyncio.sleep(1)
        
        embed = discord.Embed(
            title="🪙 Resultado da Moeda",
            description=f"{emoji} **{resultado}!**",
            color=discord.Color.gold()
        )
        
        await msg.edit(content=None, embed=embed)
    
    @commands.command(name='escolher', aliases=['choose', 'selecionar'])
    async def escolher(self, ctx, *opcoes):
        """Escolhe uma opção aleatória (separe por espaços)"""
        if len(opcoes) < 2:
            await ctx.send("❌ Forneça pelo menos 2 opções!")
            return
        
        escolha = random.choice(opcoes)
        
        embed = discord.Embed(
            title="🤔 Decisão Tomada!",
            description=f"Eu escolho: **{escolha}**",
            color=discord.Color.purple()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='8ball', aliases=['bola8'])
    async def bola8(self, ctx, *, pergunta: str):
        """Faça uma pergunta à bola 8 mágica"""
        respostas = [
            "✅ Com certeza!",
            "✅ Definitivamente sim!",
            "✅ Sem dúvida!",
            "✅ Sim, definitivamente!",
            "✅ Você pode confiar nisso!",
            "🤔 Sinais apontam para sim.",
            "🤔 Perspectivas boas.",
            "🤔 Parece que sim.",
            "🤔 Melhor não te dizer agora.",
            "🤔 Pergunte novamente mais tarde.",
            "⚠️ Não posso prever agora.",
            "⚠️ Concentre-se e pergunte novamente.",
            "❌ Não conte com isso.",
            "❌ Minha resposta é não.",
            "❌ Minhas fontes dizem que não.",
            "❌ As perspectivas não são boas.",
            "❌ Muito duvidoso."
        ]
        
        resposta = random.choice(respostas)
        
        embed = discord.Embed(
            title="🎱 Bola 8 Mágica",
            color=discord.Color.purple()
        )
        embed.add_field(name="❓ Pergunta", value=pergunta, inline=False)
        embed.add_field(name="💭 Resposta", value=resposta, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='piada', aliases=['joke'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def piada(self, ctx):
        """Conta uma piada aleatória"""
        piada = random.choice(self.piadas)
        
        embed = discord.Embed(
            title="😂 Piada do Dia",
            description=piada,
            color=discord.Color.orange()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='fato', aliases=['fact', 'curiosidade'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fato(self, ctx):
        """Mostra um fato interessante"""
        fato = random.choice(self.fatos)
        
        embed = discord.Embed(
            title="💡 Você Sabia?",
            description=fato,
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='ship', aliases=['shippar'])
    async def ship(self, ctx, pessoa1: discord.Member, pessoa2: discord.Member):
        """Calcula a compatibilidade entre duas pessoas"""
        # Gerar porcentagem consistente baseada nos IDs
        seed = pessoa1.id + pessoa2.id
        random.seed(seed)
        porcentagem = random.randint(0, 100)
        random.seed()  # Resetar seed
        
        # Determinar cor e mensagem
        if porcentagem >= 80:
            cor = discord.Color.red()
            mensagem = "💖 Casal perfeito!"
        elif porcentagem >= 60:
            cor = discord.Color.orange()
            mensagem = "💕 Boa compatibilidade!"
        elif porcentagem >= 40:
            cor = discord.Color.gold()
            mensagem = "💛 Pode funcionar..."
        elif porcentagem >= 20:
            cor = discord.Color.blue()
            mensagem = "💙 Chances baixas..."
        else:
            cor = discord.Color.dark_gray()
            mensagem = "💔 Melhor só amigos!"
        
        # Criar nome do ship
        nome1 = pessoa1.display_name[:len(pessoa1.display_name)//2]
        nome2 = pessoa2.display_name[len(pessoa2.display_name)//2:]
        ship_name = nome1 + nome2
        
        embed = discord.Embed(
            title="💘 Shipômetro",
            description=f"**{pessoa1.display_name}** + **{pessoa2.display_name}**",
            color=cor
        )
        
        # Barra de progresso
        barra_cheia = int(porcentagem / 10)
        barra_vazia = 10 - barra_cheia
        barra = "█" * barra_cheia + "░" * barra_vazia
        
        embed.add_field(
            name=f"💕 Compatibilidade: {porcentagem}%",
            value=f"`{barra}`",
            inline=False
        )
        embed.add_field(name="✨ Nome do Ship", value=f"**{ship_name}**", inline=False)
        embed.add_field(name="💬 Resultado", value=mensagem, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='emoji', aliases=['emojify'])
    async def emoji(self, ctx, *, texto: str):
        """Converte texto em emojis de letras"""
        emojis = {
            'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪',
            'f': '🇫', 'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯',
            'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴',
            'p': '🇵', 'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹',
            'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾',
            'z': '🇿', '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣',
            '4': '4️⃣', '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣',
            '9': '9️⃣', '!': '❗', '?': '❓', ' ': '   '
        }
        
        resultado = ''.join(emojis.get(char.lower(), char) for char in texto)
        
        if len(resultado) > 2000:
            await ctx.send("❌ Texto muito longo!")
            return
        
        await ctx.send(resultado)
    
    @commands.command(name='reverse', aliases=['inverter'])
    async def reverse(self, ctx, *, texto: str):
        """Inverte o texto"""
        texto_invertido = texto[::-1]
        
        embed = discord.Embed(
            title="🔄 Texto Invertido",
            description=texto_invertido,
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='mock', aliases=['zombar'])
    async def mock(self, ctx, *, texto: str):
        """Transforma o texto em mOcKiNg TeXt"""
        resultado = ''.join(
            char.upper() if i % 2 == 0 else char.lower()
            for i, char in enumerate(texto)
        )
        
        await ctx.send(resultado)
    
    @commands.command(name='contador', aliases=['count'])
    async def contador(self, ctx, segundos: int = 10):
        """Cria uma contagem regressiva"""
        if segundos < 1 or segundos > 60:
            await ctx.send("❌ O tempo deve ser entre 1 e 60 segundos!")
            return
        
        embed = discord.Embed(
            title="⏱️ Contagem Regressiva",
            description=f"**{segundos}**",
            color=discord.Color.blue()
        )
        
        msg = await ctx.send(embed=embed)
        
        for i in range(segundos - 1, 0, -1):
            await asyncio.sleep(1)
            embed.description = f"**{i}**"
            await msg.edit(embed=embed)
        
        await asyncio.sleep(1)
        embed.title = "🎉 Tempo Esgotado!"
        embed.description = "**0**"
        embed.color = discord.Color.green()
        await msg.edit(embed=embed)
    
    @commands.command(name='ascii', aliases=['arte'])
    async def ascii(self, ctx, *, texto: str):
        """Cria texto em ASCII art (máximo 10 caracteres)"""
        if len(texto) > 10:
            await ctx.send("❌ Máximo de 10 caracteres!")
            return
        
        # ASCII art simples
        resultado = f"```\n{texto.upper()}\n{'═' * len(texto) * 2}\n```"
        await ctx.send(resultado)

    # --- Slash commands ---
    @app_commands.command(name='dado', description='Rola um dado (padrão: 6 lados)')
    @app_commands.describe(lados='Número de lados do dado (2-100)')
    async def dado_slash(self, interaction: discord.Interaction, lados: int = 6):
        if lados < 2 or lados > 100:
            await interaction.response.send_message("❌ O dado deve ter entre 2 e 100 lados!", ephemeral=True)
            return
        resultado = random.randint(1, lados)
        embed = discord.Embed(title="🎲 Rolando o Dado...", description=f"**Resultado:** {resultado}", color=discord.Color.blue())
        embed.set_footer(text=f"Dado de {lados} lados")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='moeda', description='Joga uma moeda (cara ou coroa)')
    async def moeda_slash(self, interaction: discord.Interaction):
        resultado = random.choice(['Cara', 'Coroa'])
        emoji = '🪙' if resultado == 'Cara' else '💿'
        await interaction.response.send_message(f"{emoji} **{resultado}!**")

    @app_commands.command(name='escolher', description='Escolhe uma opção aleatória')
    @app_commands.describe(opcoes='Opções separadas por | (pipe). Ex: opc1|opc2|opc3')
    async def escolher_slash(self, interaction: discord.Interaction, opcoes: str):
        op_list = [o.strip() for o in opcoes.split('|') if o.strip()]
        if len(op_list) < 2:
            await interaction.response.send_message("❌ Forneça pelo menos 2 opções separadas por |", ephemeral=True)
            return
        escolha = random.choice(op_list)
        embed = discord.Embed(title="🤔 Decisão Tomada!", description=f"Eu escolho: **{escolha}**", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='8ball', description='Faça uma pergunta à bola 8 mágica')
    @app_commands.describe(pergunta='Sua pergunta')
    async def bola8_slash(self, interaction: discord.Interaction, pergunta: str):
        respostas = [
            "✅ Com certeza!","✅ Definitivamente sim!","✅ Sem dúvida!","✅ Sim, definitivamente!","✅ Você pode confiar nisso!",
            "🤔 Sinais apontam para sim.","🤔 Perspectivas boas.","🤔 Parece que sim.","🤔 Melhor não te dizer agora.","🤔 Pergunte novamente mais tarde.",
            "⚠️ Não posso prever agora.","⚠️ Concentre-se e pergunte novamente.","❌ Não conte com isso.","❌ Minha resposta é não.","❌ Minhas fontes dizem que não.","❌ As perspectivas não são boas.","❌ Muito duvidoso."
        ]
        resposta = random.choice(respostas)
        embed = discord.Embed(title="🎱 Bola 8 Mágica", color=discord.Color.purple())
        embed.add_field(name="❓ Pergunta", value=pergunta, inline=False)
        embed.add_field(name="💭 Resposta", value=resposta, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='piada', description='Conta uma piada aleatória')
    async def piada_slash(self, interaction: discord.Interaction):
        piada = random.choice(self.piadas)
        embed = discord.Embed(title="😂 Piada do Dia", description=piada, color=discord.Color.orange())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='fato', description='Mostra um fato interessante')
    async def fato_slash(self, interaction: discord.Interaction):
        fato = random.choice(self.fatos)
        embed = discord.Embed(title="💡 Você Sabia?", description=fato, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='ship', description='Calcula compatibilidade entre duas pessoas')
    @app_commands.describe(pessoa1='Primeira pessoa', pessoa2='Segunda pessoa')
    async def ship_slash(self, interaction: discord.Interaction, pessoa1: discord.Member, pessoa2: discord.Member):
        seed = pessoa1.id + pessoa2.id
        random.seed(seed)
        porcentagem = random.randint(0, 100)
        random.seed()
        if porcentagem >= 80:
            cor = discord.Color.red(); mensagem = "💖 Casal perfeito!"
        elif porcentagem >= 60:
            cor = discord.Color.orange(); mensagem = "💕 Boa compatibilidade!"
        elif porcentagem >= 40:
            cor = discord.Color.gold(); mensagem = "💛 Pode funcionar..."
        elif porcentagem >= 20:
            cor = discord.Color.blue(); mensagem = "💙 Chances baixas..."
        else:
            cor = discord.Color.dark_gray(); mensagem = "💔 Melhor só amigos!"
        nome1 = pessoa1.display_name[:len(pessoa1.display_name)//2]
        nome2 = pessoa2.display_name[len(pessoa2.display_name)//2:]
        ship_name = nome1 + nome2
        barra_cheia = int(porcentagem / 10)
        barra_vazia = 10 - barra_cheia
        barra = "█" * barra_cheia + "░" * barra_vazia
        embed = discord.Embed(title="💘 Shipômetro", description=f"**{pessoa1.display_name}** + **{pessoa2.display_name}**", color=cor)
        embed.add_field(name=f"💕 Compatibilidade: {porcentagem}%", value=f"`{barra}`", inline=False)
        embed.add_field(name="✨ Nome do Ship", value=f"**{ship_name}**", inline=False)
        embed.add_field(name="💬 Resultado", value=mensagem, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='emoji', description='Converte texto em emojis de letras')
    @app_commands.describe(texto='Texto para converter')
    async def emoji_slash(self, interaction: discord.Interaction, texto: str):
        emojis = {'a':'🇦','b':'🇧','c':'🇨','d':'🇩','e':'🇪','f':'🇫','g':'🇬','h':'🇭','i':'🇮','j':'🇯','k':'🇰','l':'🇱','m':'🇲','n':'🇳','o':'🇴','p':'🇵','q':'🇶','r':'🇷','s':'🇸','t':'🇹','u':'🇺','v':'🇻','w':'🇼','x':'🇽','y':'🇾','z':'🇿','0':'0️⃣','1':'1️⃣','2':'2️⃣','3':'3️⃣','4':'4️⃣','5':'5️⃣','6':'6️⃣','7':'7️⃣','8':'8️⃣','9':'9️⃣','!':'❗','?':'❓',' ':'   '}
        resultado = ''.join(emojis.get(char.lower(), char) for char in texto)
        if len(resultado) > 2000:
            await interaction.response.send_message("❌ Texto muito longo!", ephemeral=True)
            return
        await interaction.response.send_message(resultado)

    @app_commands.command(name='reverse', description='Inverte o texto')
    @app_commands.describe(texto='Texto a inverter')
    async def reverse_slash(self, interaction: discord.Interaction, texto: str):
        texto_invertido = texto[::-1]
        embed = discord.Embed(title="🔄 Texto Invertido", description=texto_invertido, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='mock', description='Transforma o texto em mOcKiNg TeXt')
    @app_commands.describe(texto='Texto a transformar')
    async def mock_slash(self, interaction: discord.Interaction, texto: str):
        resultado = ''.join(char.upper() if i % 2 == 0 else char.lower() for i, char in enumerate(texto))
        await interaction.response.send_message(resultado)

    @app_commands.command(name='contador', description='Cria uma contagem regressiva')
    @app_commands.describe(segundos='Segundos para contagem (1-60)')
    async def contador_slash(self, interaction: discord.Interaction, segundos: int = 10):
        if segundos < 1 or segundos > 60:
            await interaction.response.send_message("❌ O tempo deve ser entre 1 e 60 segundos!", ephemeral=True)
            return
        await interaction.response.defer()
        embed = discord.Embed(title="⏱️ Contagem Regressiva", description=f"**{segundos}**", color=discord.Color.blue())
        msg = await interaction.followup.send(embed=embed)
        for i in range(segundos - 1, 0, -1):
            await asyncio.sleep(1)
            embed.description = f"**{i}**"
            await msg.edit(embed=embed)
        await asyncio.sleep(1)
        embed.title = "🎉 Tempo Esgotado!"
        embed.description = "**0**"
        embed.color = discord.Color.green()
        await msg.edit(embed=embed)

    @app_commands.command(name='ascii', description='Cria texto em ASCII art (máximo 10 caracteres)')
    @app_commands.describe(texto='Texto (max 10 chars)')
    async def ascii_slash(self, interaction: discord.Interaction, texto: str):
        if len(texto) > 10:
            await interaction.response.send_message("❌ Máximo de 10 caracteres!", ephemeral=True)
            return
        resultado = f"```\n{texto.upper()}\n{'═' * len(texto) * 2}\n```"
        await interaction.response.send_message(resultado)

async def setup(bot):
    await bot.add_cog(Diversao(bot))

