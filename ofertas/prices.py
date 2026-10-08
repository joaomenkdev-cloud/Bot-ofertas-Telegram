"""Tratamento de preços e cálculo de desconto."""

import re

# ═════════════════════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES
# ═════════════════════════════════════════════════════════════════════════════

def parse_brl(price_text):
    """
    Converte um preço em reais para número.
    No formato brasileiro o ponto separa milhar e a vírgula separa centavos:
    "1.299" -> 1299.0, "R$ 1.299,90" -> 1299.9
    """
    price = re.sub(r'[^\d,.]', '', price_text or '')
    if not price:
        return None
    price = price.replace('.', '').replace(',', '.')
    try:
        return float(price)
    except ValueError:
        return None

def format_brl(value):
    """Formata um número como preço em reais: 1299.9 -> "R$ 1.299,90" """
    formatted = f"{value:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
    return f"R$ {formatted}"

def clean_price(price_text):
    """Limpa e formata o preço"""
    value = parse_brl(price_text)
    return format_brl(value) if value is not None else "Consultar"

def calculate_discount(original_price, current_price):
    """Calcula a porcentagem de desconto"""
    original = parse_brl(original_price)
    current = parse_brl(current_price)
    if original and current is not None and original > current:
        discount_percent = ((original - current) / original) * 100
        return f"{int(discount_percent)}% OFF"
    return None
