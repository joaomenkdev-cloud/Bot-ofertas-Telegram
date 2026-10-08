"""Filtro de produtos por palavras-chave."""

import re

from .config import ALLOWED_KEYWORDS, BLOCKED_KEYWORDS

# ═════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE FILTRO DE PRODUTOS
# ═════════════════════════════════════════════════════════════════════════════

def contains_keyword(text, keyword):
    """
    Procura a palavra-chave como palavra inteira (com plural opcional).
    Evita falsos positivos de substring, como 'ram' dentro de 'Tramontina'.
    """
    pattern = rf"(?<!\w){re.escape(keyword)}(?:e?s)?(?!\w)"
    return re.search(pattern, text) is not None

def is_pc_related_product(title):
    """
    Verifica se o produto é relacionado a tecnologia/gaming
    Retorna True se for aceito, False se for bloqueado
    """
    title_lower = title.lower()
    
    # Primeiro verifica se está bloqueado
    for blocked in BLOCKED_KEYWORDS:
        if contains_keyword(title_lower, blocked):
            print(f"  ❌ Bloqueado por: '{blocked}'")
            return False
    
    # Depois verifica se está permitido
    for keyword in ALLOWED_KEYWORDS:
        if contains_keyword(title_lower, keyword):
            print(f"  ✅ Permitido por: '{keyword}'")
            return True
    
    # Se não encontrou nenhuma palavra-chave, bloqueia
    print(f"  ⚠️ Sem palavras-chave relacionadas")
    return False
