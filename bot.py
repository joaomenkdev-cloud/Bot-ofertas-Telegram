"""
═══════════════════════════════════════════════════════════════════════════════
    BOT DE TELEGRAM - OFERTAS COM LINKS DE AFILIADO
    
    O QUE ESTE BOT FAZ?
    • Busca ofertas em várias lojas (Mercado Livre, Amazon, Shopee, etc)
    • Transforma links normais em links de afiliado (para você ganhar comissão)
    • Envia ofertas automaticamente no seu grupo do Telegram
    • Evita duplicatas (não envia a mesma oferta duas vezes)
    • Sistema de fila inteligente
    
    COMO USAR?
    1. Instale as bibliotecas: pip install python-telegram-bot selenium webdriver-manager beautifulsoup4 lxml mysql-connector-python
    2. Configure seus IDs de afiliado na seção "CONFIGURAÇÃO DE AFILIADOS" abaixo
    3. Configure o token do bot e ID do grupo
    4. Execute: python bot.py
    
    IMPORTANTE:
    • Você precisa ter o Google Chrome instalado
    • Você precisa ter o MySQL instalado e rodando
    • Cadastre-se nos programas de afiliados antes de usar
═══════════════════════════════════════════════════════════════════════════════
"""

from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler

from ofertas.commands import buscar_ofertas_command, config_command, status_command
from ofertas.config import AFFILIATE_CONFIG, BOT_TOKEN
from ofertas.database import initialize_database
from ofertas.jobs import check_and_search_if_needed, send_queued_offers
from ofertas.scheduling import get_offers_per_hour, get_send_interval

# ═════════════════════════════════════════════════════════════════════════════
# INICIALIZAÇÃO
# ═════════════════════════════════════════════════════════════════════════════

def main():
    """Função principal - Inicia o bot"""
    
    print("="*60)
    print("🤖 BOT DE OFERTAS COM SISTEMA DE AFILIADOS")
    print("="*60)
    print(f"📅 Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*60)
    
    # Inicializa o banco de dados
    initialize_database()
    
    # Verifica configuração de afiliados
    print("\n🔍 Verificando configuração de afiliados...")
    for platform, config in AFFILIATE_CONFIG.items():
        if config.get('enabled'):
            if config.get('id') and not config['id'].startswith('SEU_ID_'):
                print(f"  ✅ {platform.upper()}: Configurado")
            else:
                print(f"  ⚠️ {platform.upper()}: ID não configurado!")
        else:
            print(f"  ❌ {platform.upper()}: Desabilitado")
    
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
    
    # Envia ofertas da fila com intervalo dinâmico
    # Calcula automaticamente baseado no horário
    interval = get_send_interval()
    application.job_queue.run_repeating(send_queued_offers, interval=interval, first=30)
    
    # Atualiza o intervalo a cada hora para se adaptar ao horário
    async def update_send_interval(context):
        """Atualiza o intervalo de envio baseado no horário atual"""
        new_interval = get_send_interval()
        offers_per_hour = get_offers_per_hour()
        print(f"\n🔄 Intervalo atualizado: {offers_per_hour} ofertas/hora")
        
        # Cancela o job antigo
        current_jobs = context.job_queue.get_jobs_by_name('send_offers')
        for job in current_jobs:
            job.schedule_removal()
        
        # Cria novo job com intervalo atualizado
        context.job_queue.run_repeating(
            send_queued_offers, 
            interval=new_interval, 
            first=1,
            name='send_offers'
        )
    
    # Atualiza o intervalo a cada hora
    application.job_queue.run_repeating(update_send_interval, interval=3600, first=3600)
    
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
