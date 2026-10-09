"""
═══════════════════════════════════════════════════════════════════════════════
    BOT DE TELEGRAM - OFERTAS COM LINKS DE AFILIADO
    
    O QUE ESTE BOT FAZ?
    • Busca ofertas no Mercado Livre (informática, celulares, TVs, games)
    • Acrescenta seus parâmetros de afiliado ao link, se configurados
    • Envia ofertas automaticamente no seu grupo do Telegram
    • Evita duplicatas (não envia a mesma oferta duas vezes)
    • Sistema de fila inteligente
    
    COMO USAR?
    1. Instale as bibliotecas: pip install -r requirements.txt
    2. Copie .env.example para .env e preencha o token do bot e o ID do grupo
    3. (Opcional) Configure seus parâmetros de afiliado no .env
    4. Execute: python bot.py
    
    IMPORTANTE:
    • Você precisa ter o Google Chrome instalado
    • Afiliado é opcional: sem ele, o bot envia o link normal do produto
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler

from ofertas.affiliates import is_affiliate_configured
from ofertas.commands import buscar_ofertas_command, config_command, status_command
from ofertas.config import ADMIN_IDS, AFFILIATE_CONFIG, BOT_TOKEN, GROUP_CHAT_ID
from ofertas.database import initialize_database
from ofertas.jobs import check_and_search_if_needed, send_queued_offers
from ofertas.scheduling import get_offers_per_hour, get_send_interval

# ═════════════════════════════════════════════════════════════════════════════
# INICIALIZAÇÃO
# ═════════════════════════════════════════════════════════════════════════════

def main():
    """Função principal - Inicia o bot"""

    # No Windows, com a saída redirecionada (arquivo de log, serviço, agendador),
    # o Python usa cp1252 e o primeiro print com emoji derruba o bot.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    if "--login" in sys.argv:
        from ofertas.scraper import login_interactive
        login_interactive()
        return

    print("="*60)
    print("🤖 BOT DE OFERTAS COM SISTEMA DE AFILIADOS")
    print("="*60)
    print(f"📅 Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*60)
    
    if not BOT_TOKEN or not GROUP_CHAT_ID:
        print("❌ BOT_TOKEN e GROUP_CHAT_ID precisam estar no arquivo .env")
        print("💡 Copie o .env.example para .env e preencha os valores")
        sys.exit(1)

    if not ADMIN_IDS:
        print("⚠️ ADMIN_IDS vazio no .env: os comandos /buscar, /status e /config ficam desativados")

    # Inicializa o banco de dados
    initialize_database()
    
    # Verifica configuração de afiliados
    print("\n🔍 Verificando configuração de afiliados...")
    for platform in AFFILIATE_CONFIG:
        if is_affiliate_configured(platform):
            print(f"  ✅ {platform.upper()}: Configurado")
        else:
            print(f"  ➖ {platform.upper()}: sem afiliado, envia o link direto do produto")
    
    # Cria a aplicação
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Adiciona comandos
    application.add_handler(CommandHandler("buscar", buscar_ofertas_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("config", config_command))
    
    # ══════════════════════════════════════════════════════════════════════════
    # AGENDAMENTO INTELIGENTE
    # ══════════════════════════════════════════════════════════════════════════
    # O bot se adapta ao horário:
    # - Horários normais: 6 ofertas/hora (a cada 10 minutos)
    # - Horários de pico: 12 ofertas/hora (a cada 5 minutos)
    #
    # Horários de pico:
    # - 8h-10h (manhã)
    # - 12h-14h (almoço)
    # - 18h-22h (noite)
    # - Finais de semana: 14h-22h
    # ══════════════════════════════════════════════════════════════════════════
    
    # Um único job confere a cada minuto se já passou o intervalo do horário
    # atual (muda sozinho entre pico e fora de pico) e envia uma oferta.
    application.job_queue.run_repeating(send_queued_offers, interval=60, first=30)
    
    # Verifica e busca novas ofertas a cada 30 minutos
    application.job_queue.run_repeating(check_and_search_if_needed, interval=1800, first=60)
    
    print("\n" + "="*60)
    print("✅ BOT INICIADO COM SUCESSO!")
    print("="*60)
    print(f"📊 Modo inicial: {get_offers_per_hour()} ofertas/hora")
    print(f"⏰ Intervalo atual: {get_send_interval()} segundos entre envios")
    print("🔄 Verificação automática: a cada 30 minutos")
    print("\n📱 COMANDOS DISPONÍVEIS:")
    print("  /buscar - Busca ofertas manualmente")
    print("  /status - Mostra estatísticas")
    print("  /config - Mostra configuração de afiliados")
    print("\n⏰ SISTEMA DE ENVIO INTELIGENTE:")
    print("  • Horários normais: 6 ofertas/hora (a cada 10min)")
    print("  • Horários de pico: 12 ofertas/hora (a cada 5min)")
    print("  • Picos: 8-10h, 12-14h, 18-22h + fins de semana")
    print("="*60 + "\n")
    
    # Inicia o bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
