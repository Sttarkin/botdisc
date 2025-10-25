from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import json
import os
import asyncio
import threading
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Variável global para o bot (será definida pelo main.py)
bot_instance = None

def load_server_configs():
    """Carregar configurações dos servidores"""
    try:
        with open('server_configs.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_server_configs(configs):
    """Salvar configurações dos servidores"""
    with open('server_configs.json', 'w', encoding='utf-8') as f:
        json.dump(configs, f, indent=2, ensure_ascii=False)

def get_bot_guilds():
    """Obter lista de servidores do bot"""
    if not bot_instance:
        return []
    
    guilds = []
    for guild in bot_instance.guilds:
        guilds.append({
            'id': str(guild.id),
            'name': guild.name,
            'icon': str(guild.icon.url) if guild.icon else None,
            'member_count': guild.member_count,
            'owner_id': str(guild.owner_id)
        })
    return guilds

def get_guild_channels(guild_id):
    """Obter canais de um servidor"""
    if not bot_instance:
        return []
    
    guild = bot_instance.get_guild(int(guild_id))
    if not guild:
        return []
    
    channels = []
    for channel in guild.channels:
        if hasattr(channel, 'name'):
            channels.append({
                'id': str(channel.id),
                'name': channel.name,
                'type': str(channel.type),
                'category': channel.category.name if channel.category else None
            })
    return channels

@app.route('/')
def index():
    """Página principal do dashboard"""
    return render_template('index.html')

@app.route('/api/guilds')
def api_guilds():
    """API para obter servidores do bot"""
    return jsonify(get_bot_guilds())

@app.route('/api/guild/<guild_id>')
def api_guild(guild_id):
    """API para obter informações de um servidor específico"""
    guilds = get_bot_guilds()
    guild = next((g for g in guilds if g['id'] == guild_id), None)
    
    if not guild:
        return jsonify({'error': 'Servidor não encontrado'}), 404
    
    # Adicionar canais
    guild['channels'] = get_guild_channels(guild_id)
    
    # Adicionar configurações atuais
    configs = load_server_configs()
    guild['config'] = configs.get(guild_id, {
        'enabled_channels': [],
        'welcome_channel': None,
        'welcome_message': 'Bem-vindo ao servidor, {user}!',
        'custom_commands': {},
        'ai_enabled': True,
        'moderation_enabled': True,
        'economy_enabled': True,
        'levels_enabled': True
    })
    
    return jsonify(guild)

@app.route('/api/guild/<guild_id>/config', methods=['GET', 'POST'])
def api_guild_config(guild_id):
    """API para obter/atualizar configurações de um servidor"""
    configs = load_server_configs()
    
    if request.method == 'GET':
        return jsonify(configs.get(guild_id, {}))
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Validar dados
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        # Atualizar configurações
        configs[guild_id] = {
            'enabled_channels': data.get('enabled_channels', []),
            'welcome_channel': data.get('welcome_channel'),
            'welcome_message': data.get('welcome_message', 'Bem-vindo ao servidor, {user}!'),
            'custom_commands': data.get('custom_commands', {}),
            'ai_enabled': data.get('ai_enabled', True),
            'moderation_enabled': data.get('moderation_enabled', True),
            'economy_enabled': data.get('economy_enabled', True),
            'levels_enabled': data.get('levels_enabled', True),
            'last_updated': datetime.now().isoformat()
        }
        
        save_server_configs(configs)
        
        # Notificar o bot sobre as mudanças (sem asyncio)
        if bot_instance:
            print(f"[DASHBOARD] Configurações atualizadas para servidor {guild_id}")
        
        return jsonify({'success': True, 'config': configs[guild_id]})

@app.route('/api/guild/<guild_id>/custom-commands', methods=['GET', 'POST', 'DELETE'])
def api_custom_commands(guild_id):
    """API para gerenciar comandos personalizados"""
    configs = load_server_configs()
    guild_config = configs.get(guild_id, {})
    custom_commands = guild_config.get('custom_commands', {})
    
    if request.method == 'GET':
        return jsonify(custom_commands)
    
    elif request.method == 'POST':
        data = request.get_json()
        command_name = data.get('name')
        command_response = data.get('response')
        
        if not command_name or not command_response:
            return jsonify({'error': 'Nome e resposta são obrigatórios'}), 400
        
        custom_commands[command_name] = {
            'response': command_response,
            'created_at': datetime.now().isoformat(),
            'usage_count': 0
        }
        
        configs[guild_id]['custom_commands'] = custom_commands
        save_server_configs(configs)
        
        return jsonify({'success': True, 'command': custom_commands[command_name]})
    
    elif request.method == 'DELETE':
        command_name = request.args.get('name')
        
        if not command_name or command_name not in custom_commands:
            return jsonify({'error': 'Comando não encontrado'}), 404
        
        del custom_commands[command_name]
        configs[guild_id]['custom_commands'] = custom_commands
        save_server_configs(configs)
        
        return jsonify({'success': True})

@app.route('/api/bot/status')
def api_bot_status():
    """API para obter status do bot"""
    if not bot_instance:
        return jsonify({'online': False, 'error': 'Bot não conectado'})
    
    return jsonify({
        'online': True,
        'guilds': len(bot_instance.guilds),
        'users': len(bot_instance.users),
        'uptime': time.time() - bot_instance.start_time if hasattr(bot_instance, 'start_time') else 0,
        'latency': bot_instance.latency
    })

def update_bot_config(guild_id, config):
    """Atualizar configurações do bot em tempo real"""
    # Esta função será chamada quando as configurações forem atualizadas
    print(f"[DASHBOARD] Configurações atualizadas para servidor {guild_id}")

def run_dashboard(host='0.0.0.0', port=5000):
    """Executar o dashboard"""
    print(f"[DASHBOARD] Iniciando dashboard em http://{host}:{port}")
    app.run(host=host, port=port, debug=False, threaded=True)

def set_bot_instance(bot):
    """Definir instância do bot"""
    global bot_instance
    bot_instance = bot

if __name__ == '__main__':
    run_dashboard()
