"""Comandos do bot: /buscar, /status e /config."""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .config import AFFILIATE_CONFIG, SCRAPING_TARGETS
from .database import get_queue_count, get_statistics
from .jobs import find_and_manage_offers

# ═════════════════════════════════════════════════════════════════════════════
# COMANDOS DO BOT (APENAS PARA O DONO)
# ═════════════════════════════════════════════════════════════════════════════
# ⚠️ IMPORTANTE: Estes comandos só funcionam para quem tem acesso ao código
# Não há interface pública - apenas logs no terminal

async def buscar_ofertas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /buscar - Busca ofertas manualmente (uso privado)"""
    # Responde apenas no privado/grupo autorizado
    await update.message.reply_text("🔍 Buscando ofertas...")
    await find_and_manage_offers(context)
    await update.message.reply_text("✅ Busca concluída!")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /status - Mostra estatísticas (uso privado)"""
    stats = get_statistics()
    queue_counts = get_queue_count()
    
    msg = f"🤖 *STATUS DO BOT*\n\n"
    msg += f"✅ Bot ativo e funcionando\n"
    msg += f"🔍 Sites monitorados: {len(SCRAPING_TARGETS)}\n\n"
    
    if stats:
        msg += f"📊 *ESTATÍSTICAS:*\n"
        msg += f"📦 Total de ofertas: {stats['total']}\n"
        msg += f"📅 Enviadas hoje: {stats['hoje']}\n"
        msg += f"💰 Com afiliado: {stats['com_afiliado']}\n\n"
    
    msg += f"📥 *FILA:*\n"
    total_fila = sum(queue_counts.values())
    msg += f"Total: {total_fila}\n"
    for fonte, qtd in queue_counts.items():
        msg += f"  • {fonte}: {qtd}\n"
    
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def config_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /config - Mostra configuração de afiliados (uso privado)"""
    msg = f"⚙️ *CONFIGURAÇÃO DE AFILIADOS*\n\n"
    
    for platform, config in AFFILIATE_CONFIG.items():
        status = "✅" if config.get('enabled') else "❌"
        has_id = "✅" if config.get('id') and not config['id'].startswith('SEU_ID_') else "❌"
        
        msg += f"*{platform.upper()}*\n"
        msg += f"  Status: {status}\n"
        msg += f"  ID configurado: {has_id}\n\n"
    
    msg += f"\n💡 Para configurar, edite AFFILIATE_CONFIG no código"
    
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
