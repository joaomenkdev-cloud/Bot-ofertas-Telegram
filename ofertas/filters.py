"""Filtro de produtos por palavras-chave."""

from .config import ALLOWED_KEYWORDS, BLOCKED_KEYWORDS

# ═════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE FILTRO DE PRODUTOS
# ═════════════════════════════════════════════════════════════════════════════

def is_pc_related_product(title):
    """
    Verifica se o produto é relacionado a tecnologia/gaming
    Retorna True se for aceito, False se for bloqueado
    """
    title_lower = title.lower()
    
    # Primeiro verifica se está bloqueado
    for blocked in BLOCKED_KEYWORDS:
        if blocked in title_lower:
            print(f"  ❌ Bloqueado por: '{blocked}'")
            return False
    
    # Depois verifica se está permitido
    for keyword in ALLOWED_KEYWORDS:
        if keyword in title_lower:
            print(f"  ✅ Permitido por: '{keyword}'")
            return True
    
    # Se não encontrou nenhuma palavra-chave, bloqueia
    print(f"  ⚠️ Sem palavras-chave relacionadas")
    return False
