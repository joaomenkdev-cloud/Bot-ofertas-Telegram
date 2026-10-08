"""Tratamento de preços e cálculo de desconto."""

import re

# ═════════════════════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES
# ═════════════════════════════════════════════════════════════════════════════

def clean_price(price_text):
    """Limpa e formata o preço"""
    price = re.sub(r'[^\d,.]', '', price_text)
    if '.' in price and ',' in price:
        price = price.replace('.', '').replace(',', '.')
    return f"R$ {price}" if price else "Consultar"

def calculate_discount(original_price, current_price):
    """Calcula a porcentagem de desconto"""
    try:
        original = float(re.sub(r'[^\d.]', '', original_price))
        current = float(re.sub(r'[^\d.]', '', current_price))
        if original > current:
            discount_percent = ((original - current) / original) * 100
            return f"{int(discount_percent)}% OFF"
    except:
        pass
    return None
