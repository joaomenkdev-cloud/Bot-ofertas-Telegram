"""Detecção de plataforma e geração de links de afiliado (opcional)."""

from urllib.parse import urlsplit, urlunsplit

from .config import AFFILIATE_CONFIG

# ═════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DO SISTEMA DE AFILIADOS
# ═════════════════════════════════════════════════════════════════════════════

def detect_platform(url):
    """
    Detecta qual plataforma é a URL
    Retorna o nome da plataforma ou None se não reconhecer
    """
    url_lower = url.lower()

    # Dicionário de domínios conhecidos
    platforms = {
        'mercadolivre.com': 'mercadolivre',
        'mercadolibre.com': 'mercadolivre',
        'amazon.com': 'amazon',
    }

    for domain, platform in platforms.items():
        if domain in url_lower:
            return platform

    return None

def is_affiliate_configured(platform):
    """Diz se há parâmetros de afiliado configurados para a plataforma"""
    return bool(AFFILIATE_CONFIG.get(platform, {}).get('params'))

def create_affiliate_link(original_link, platform_override=None):
    """
    Acrescenta os parâmetros de afiliado da plataforma ao link do produto.

    Sem afiliado configurado, devolve o link original: a oferta é enviada
    normalmente, só não gera comissão.
    """
    platform = platform_override or detect_platform(original_link)
    params = AFFILIATE_CONFIG.get(platform, {}).get('params', '').strip().lstrip('?&')
    if not params:
        return original_link

    scheme, netloc, path, query, fragment = urlsplit(original_link)
    query = f"{query}&{params}" if query else params
    return urlunsplit((scheme, netloc, path, query, fragment))
