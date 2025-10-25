"""Script para verificar a sintaxe de todos os arquivos Python"""
import py_compile
import os

arquivos = [
    'main.py',
    'cogs/basicos.py',
    'cogs/moderacao.py',
    'cogs/diversao.py',
    'cogs/jogos.py',
    'cogs/economia.py',
    'cogs/niveis.py'
]

print("=" * 50)
print("VERIFICANDO SINTAXE DOS ARQUIVOS PYTHON")
print("=" * 50)

erros = []
for arquivo in arquivos:
    try:
        py_compile.compile(arquivo, doraise=True)
        print(f"✅ {arquivo} - OK")
    except py_compile.PyCompileError as e:
        print(f"❌ {arquivo} - ERRO")
        erros.append((arquivo, str(e)))

print("\n" + "=" * 50)
if not erros:
    print("🎉 TODOS OS ARQUIVOS ESTÃO CORRETOS!")
    print("=" * 50)
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Instale as dependências: py -m pip install -r requirements.txt")
    print("2. Crie o arquivo .env com seu token do Discord")
    print("3. Execute o bot: py main.py")
else:
    print("❌ ERROS ENCONTRADOS:")
    print("=" * 50)
    for arquivo, erro in erros:
        print(f"\n{arquivo}:")
        print(erro)

