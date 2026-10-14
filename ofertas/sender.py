"""Envio das ofertas para o grupo do Telegram."""

from datetime import datetime
from html import escape

from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .config import GROUP_CHAT_ID

# ═════════════════════════════════════════════════════════════════════════════
# ENVIO PARA O TELEGRAM
# ═════════════════════════════════════════════════════════════════════════════
# As mensagens usam HTML: o Markdown legado do Telegram não tem riscado e
# quebra quando o título do produto tem _, * ou [

def build_caption(offer):
    """Monta a legenda da oferta em HTML (com o texto do produto escapado)"""
    caption = "🔥 <b>OFERTA ENCONTRADA</b> 🔥\n"
    caption += "━━━━━━━━━━━━━━━━━━━━\n\n"
    caption += f"📦 <b>{escape(offer['title'])}</b>\n\n"
    
    # Preço
    if offer.get('original_price') and offer.get('discount'):
        caption += f"💰 <s>{escape(offer['original_price'])}</s> ➜ <b>{escape(offer['price'])}</b>\n"
        caption += f"🏷️ <b>{escape(offer['discount'])}</b>\n\n"
    else:
        caption += f"💰 <b>{escape(offer['price'])}</b>\n\n"
    
    # Link
    caption += f'🛒 <a href="{escape(offer["link"], quote=True)}">👉 COMPRAR AGORA</a>\n\n'
    
    # Informações básicas (SEM mencionar afiliado)
    caption += f"📍 {escape(offer['source'])}\n"
    caption += f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    return caption

async def send_offer_to_group(context: ContextTypes.DEFAULT_TYPE, offer):
    """Envia oferta para o grupo do Telegram"""
    
    # ⚠️ VALIDAÇÃO: a oferta é enviada como foto, então precisa de imagem
    if not offer.get('image_url'):
        print(f"  ❌ BLOQUEADO: Sem imagem - {offer['title'][:50]}...")
        return False
    
    try:
        await context.bot.send_photo(
            chat_id=GROUP_CHAT_ID,
            photo=offer['image_url'],
            caption=build_caption(offer),
            parse_mode=ParseMode.HTML
        )
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar: {e}")
        return False
