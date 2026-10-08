"""Envio das ofertas para o grupo do Telegram."""

from datetime import datetime

from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .config import GROUP_CHAT_ID

# ═════════════════════════════════════════════════════════════════════════════
# ENVIO PARA O TELEGRAM
# ═════════════════════════════════════════════════════════════════════════════

async def send_offer_to_group(context: ContextTypes.DEFAULT_TYPE, offer):
    """Envia oferta para o grupo do Telegram"""
    
    # ⚠️ VALIDAÇÃO: a oferta é enviada como foto, então precisa de imagem
    if not offer.get('image_url'):
        print(f"  ❌ BLOQUEADO: Sem imagem - {offer['title'][:50]}...")
        return False
    
    # Monta a mensagem
    caption = f"🔥 *OFERTA ENCONTRADA* 🔥\n"
    caption += "━━━━━━━━━━━━━━━━━━━━\n\n"
    caption += f"📦 *{offer['title']}*\n\n"
    
    # Preço
    if offer.get('original_price') and offer.get('discount'):
        caption += f"💰 ~~{offer['original_price']}~~ ➜ *{offer['price']}*\n"
        caption += f"🏷️ *{offer['discount']}*\n\n"
    else:
        caption += f"💰 *{offer['price']}*\n\n"
    
    # Link
    caption += f"🛒 [👉 COMPRAR AGORA]({offer['link']})\n\n"
    
    # Informações básicas (SEM mencionar afiliado)
    caption += f"📍 {offer['source']}\n"
    caption += f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    
    try:
        # Envia SEMPRE com imagem (já validamos acima)
        await context.bot.send_photo(
            chat_id=GROUP_CHAT_ID,
            photo=offer['image_url'],
            caption=caption,
            parse_mode=ParseMode.MARKDOWN
        )
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar: {e}")
        return False
