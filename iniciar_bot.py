"""Script auxiliar para iniciar o bot"""
import os
import sys
import subprocess

# Obter o diretório deste script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("=" * 50)
print("🤖 INICIANDO BOT DE DISCORD")
print("=" * 50)
print(f"📁 Diretório: {script_dir}")
print()

# Verificar se as dependências estão instaladas
try:
    import discord
    print("✅ discord.py instalado")
except ImportError:
    print("❌ discord.py não encontrado!")
    print("\n📦 Instalando dependências...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print()

# Verificar se o arquivo .env existe
if not os.path.exists('.env'):
    print("⚠️  ATENÇÃO: Arquivo .env não encontrado!")
    print()
    print("📝 Crie um arquivo .env com o seguinte conteúdo:")
    print("   DISCORD_TOKEN=seu_token_aqui")
    print()
    print("🔗 Obtenha seu token em:")
    print("   https://discord.com/developers/applications")
    print()
    input("Pressione ENTER depois de criar o arquivo .env...")
    print()

# Executar o bot
print("🚀 Iniciando bot...")
print("=" * 50)
print()

try:
    subprocess.run([sys.executable, "main.py"])
except KeyboardInterrupt:
    print("\n\n⏹️  Bot encerrado pelo usuário")
except Exception as e:
    print(f"\n\n❌ Erro ao executar: {e}")
    input("\nPressione ENTER para sair...")

