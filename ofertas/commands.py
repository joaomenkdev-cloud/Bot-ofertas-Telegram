"""Comandos do bot: /buscar, /status e /config."""

import functools

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .config import ADMIN_IDS, AFFILIATE_CONFIG, SCRAPING_TARGETS
from .affiliates import is_affiliate_configured
from .database import get_queue_count, get_statistics
from .jobs import find_and_manage_offers

# ═════════════════════════════════════════════════════════════════════════════
# COMANDOS DO BOT (APENAS PARA O DONO)
# ═════════════════════════════════════════════════════════════════════════════
# Só respondem a quem está em ADMIN_IDS (arquivo .env). Para qualquer outra
# pessoa o bot fica em silêncio e só registra a tentativa no terminal.

def admin_only(handler):
    """Ignora o comando se quem mandou não estiver em ADMIN_IDS"""
    @functools.wraps(handler)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if user is None or user.id not in ADMIN_IDS:
            user_id = user.id if user else "desconhecido"
            print(f"🔒 Comando ignorado: usuário {user_id} não está em ADMIN_IDS")
            return
        return await handler(update, context)
    return wrapper

@admin_only
async def buscar_ofertas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /buscar - Busca ofertas manualmente (uso privado)"""
    await update.message.reply_text("🔍 Buscando ofertas...")
    await find_and_manage_offers(context)
    await update.message.reply_text("✅ Busca concluída!")

@admin_only
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

@admin_only
async def config_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /config - Mostra configuração de afiliados (uso privado)"""
    msg = f"⚙️ *CONFIGURAÇÃO DE AFILIADOS*\n\n"
    
    for platform in AFFILIATE_CONFIG:
        status = "✅ configurado" if is_affiliate_configured(platform) else "➖ link direto (sem comissão)"
        msg += f"*{platform.upper()}*: {status}\n"
    
    msg += f"\n💡 Para configurar, preencha ML_AFFILIATE_PARAMS / AMAZON_AFFILIATE_TAG no .env"
    
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
