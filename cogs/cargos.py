import discord
from discord.ext import commands
from discord import app_commands
import json

CARGOS_CONFIG = {
    "Administrativos": {
        "👑 • Fundador": 0xFF0000,
        "🛡️ • Administrador": 0xFF3333,
        "⚔️ • Moderador": 0xFF6666,
        "🔨 • Moderador Trainee": 0xFF9999,
        "🤖 • Bot Manager": 0xFFCCCC
    },
    "Equipe": {
        "🎨 • Designer": 0x00FF00,
        "📢 • Divulgador": 0x33FF33,
        "🎬 • Editor de Vídeo": 0x66FF66,
        "✍️ • Redator": 0x99FF99,
        "🎭 • Criador de Conteúdo": 0xCCFFCC,
        "🎵 • DJ/Music Manager": 0xE6FFE6
    },
    "Especiais": {
        "💎 • VIP": 0x0000FF,
        "🌟 • Booster": 0x3333FF,
        "🎖️ • Membro Verificado": 0x6666FF,
        "🏆 • Veterano": 0x9999FF,
        "🎁 • Apoiador": 0xCCCCFF,
        "🔥 • Membro Ativo": 0xE6E6FF
    },
    "Atividades": {
        "🎮 • Gamer": 0xFF00FF,
        "📚 • Leitor": 0xFF33FF,
        "🎬 • Cinéfilo": 0xFF66FF,
        "🎵 • Melômano": 0xFF99FF,
        "🖌️ • Artista": 0xFFCCFF,
        "💻 • Programador": 0xFFE6FF,
        "⚽ • Esportista": 0xF2F2F2
    },
    "Interação": {
        "💬 • Conversador": 0xFFFF00,
        "😂 • Memer": 0xFFFF33,
        "🎤 • Palestrante": 0xFFFF66,
        "🎲 • Jogador de RPG": 0xFFFF99
    },
    "Cores": {
        "❤️ • Vermelho": 0xFF0000,
        "💙 • Azul": 0x0000FF,
        "💚 • Verde": 0x00FF00,
        "💛 • Amarelo": 0xFFFF00,
        "💜 • Roxo": 0x800080,
        "🧡 • Laranja": 0xFFA500,
        "🩷 • Rosa": 0xFFC0CB,
        "🤍 • Branco": 0xFFFFFF
    },
    "Notificações": {
        "🔔 • Anúncios": 0xFFA500,
        "🎉 • Eventos": 0xFF69B4,
        "📰 • Novidades": 0x4169E1
    }
}

class Cargos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='gerar')
    @commands.has_permissions(administrator=True)
    async def gerar_cargos(self, ctx):
        guild = ctx.guild
        criados = 0
        atualizados = 0
        erros = 0
        
        # Lista de cargos já existentes
        cargos_existentes = {cargo.name: cargo for cargo in guild.roles}
        
        # Criar cargos por categoria
        for categoria, cargos in CARGOS_CONFIG.items():
            # Criar cargo de categoria (separador)
            categoria_nome = f"👑 {categoria}" if categoria == "Administrativos" else f"{'🎨' if categoria == 'Equipe' else '⭐' if categoria == 'Especiais' else '🎮' if categoria == 'Atividades' else '💬' if categoria == 'Interação' else '🌈' if categoria == 'Cores' else '📢'} {categoria}"
            try:
                if categoria_nome not in cargos_existentes:
                    await guild.create_role(
                        name=categoria_nome,
                        color=discord.Color(0x2F3136),
                        hoist=True,
                        mentionable=False
                    )
                    criados += 1
            except Exception as e:
                print(f"Erro ao criar cargo de categoria {categoria_nome}: {e}")
                erros += 1
            
            # Criar cargos da categoria
            for nome_cargo, cor in cargos.items():
                try:
                    if nome_cargo in cargos_existentes:
                        cargo = cargos_existentes[nome_cargo]
                        if cargo.color.value != cor:
                            await cargo.edit(color=discord.Color(cor))
                            atualizados += 1
                    else:
                        await guild.create_role(
                            name=nome_cargo,
                            color=discord.Color(cor),
                            mentionable=True
                        )
                        criados += 1
                except Exception as e:
                    print(f"Erro ao criar/atualizar cargo {nome_cargo}: {e}")
                    erros += 1
        
        embed = discord.Embed(
            title="🔄 Atualização de Cargos",
            color=discord.Color.green()
        )
        embed.add_field(name="✅ Cargos Criados", value=str(criados), inline=True)
        embed.add_field(name="📝 Cargos Atualizados", value=str(atualizados), inline=True)
        if erros > 0:
            embed.add_field(name="❌ Erros", value=str(erros), inline=True)
        
        await ctx.send(embed=embed)

    @app_commands.command(name='lista_cargos', description='Mostra todos os cargos disponíveis')
    async def lista_cargos(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📋 Lista de Cargos",
            description="Lista de todos os cargos disponíveis no servidor",
            color=discord.Color.blue()
        )
        
        for categoria, cargos in CARGOS_CONFIG.items():
            valor = "\n".join(f"{nome}" for nome in cargos.keys())
            if categoria == "Administrativos":
                titulo = "👑 Cargos Administrativos"
            elif categoria == "Equipe":
                titulo = "🎨 Cargos de Equipe"
            elif categoria == "Especiais":
                titulo = "⭐ Cargos de Membros Especiais"
            elif categoria == "Atividades":
                titulo = "🎮 Cargos de Atividades"
            elif categoria == "Interação":
                titulo = "💬 Cargos de Interação"
            elif categoria == "Cores":
                titulo = "🌈 Cargos de Cores/Personalização"
            else:
                titulo = "📢 Notificações"
            
            embed.add_field(name=titulo, value=valor, inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='cargo', description='Atribui ou remove um cargo')
    @app_commands.describe(cargo='Nome do cargo que deseja receber/remover')
    async def cargo(self, interaction: discord.Interaction, cargo: str):
        # Verificar se o cargo existe na configuração
        cargo_encontrado = None
        for categoria, cargos in CARGOS_CONFIG.items():
            if cargo in cargos:
                cargo_encontrado = cargo
                break
        
        if not cargo_encontrado:
            await interaction.response.send_message(
                "❌ Cargo não encontrado! Use `/lista_cargos` para ver os cargos disponíveis.",
                ephemeral=True
            )
            return
        
        # Buscar o cargo no servidor
        guild_cargo = discord.utils.get(interaction.guild.roles, name=cargo)
        if not guild_cargo:
            await interaction.response.send_message(
                "❌ Este cargo ainda não foi criado no servidor. Peça para um administrador usar `/criar_cargos`.",
                ephemeral=True
            )
            return
        
        # Verificar permissões especiais
        if cargo.startswith(("👑", "🛡️", "⚔️", "🔨", "🤖")):  # Cargos administrativos
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message(
                    "❌ Você não pode atribuir/remover cargos administrativos!",
                    ephemeral=True
                )
                return
        
        # Adicionar ou remover o cargo
        try:
            if guild_cargo in interaction.user.roles:
                await interaction.user.remove_roles(guild_cargo)
                await interaction.response.send_message(
                    f"✅ Cargo {cargo} removido com sucesso!",
                    ephemeral=True
                )
            else:
                await interaction.user.add_roles(guild_cargo)
                await interaction.response.send_message(
                    f"✅ Cargo {cargo} adicionado com sucesso!",
                    ephemeral=True
                )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Não tenho permissão para gerenciar este cargo!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Erro ao modificar cargo: {str(e)}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Cargos(bot))