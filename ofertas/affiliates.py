"""Detecção de plataforma e geração de links de afiliado."""

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
        'shopee.com': 'shopee',
        'aliexpress.com': 'aliexpress',
        'magazineluiza.com': 'magalu',
        'americanas.com': 'americanas',
        'shein.com': 'shein',
    }
    
    for domain, platform in platforms.items():
        if domain in url_lower:
            return platform
    
    return None

def create_affiliate_link(original_link, platform_override=None):
    """
    Transforma um link normal em link de afiliado
    
    Args:
        original_link: Link original do produto
        platform_override: Forçar uma plataforma específica (opcional)
    
    Returns:
        Link de afiliado ou link original se não tiver cadastro
    """
    # Detecta a plataforma
    platform = platform_override or detect_platform(original_link)
    
    if not platform:
        print(f"  ⚠️ AVISO: Plataforma não identificada no link: {original_link[:50]}")
        print(f"  ℹ️ Link será enviado sem afiliação (você não ganhará comissão)")
        return original_link
    
    # Verifica se tem configuração de afiliado para esta plataforma
    if platform not in AFFILIATE_CONFIG:
        print(f"  ⚠️ AVISO: Plataforma '{platform}' não configurada em AFFILIATE_CONFIG")
        print(f"  ℹ️ Link será enviado sem afiliação (você não ganhará comissão)")
        return original_link
    
    config = AFFILIATE_CONFIG[platform]
    
    # Verifica se o afiliado está habilitado
    if not config.get('enabled', False):
        print(f"  ⚠️ AVISO: Afiliado da plataforma '{platform}' está desabilitado")
        print(f"  ℹ️ Link será enviado sem afiliação (você não ganhará comissão)")
        return original_link
    
    # Verifica se tem ID configurado
    affiliate_id = config.get('id', '')
    if not affiliate_id or affiliate_id.startswith('SEU_ID_'):
        print(f"  ⚠️ AVISO: ID de afiliado da plataforma '{platform}' não configurado!")
        print(f"  ℹ️ Configure seu ID em AFFILIATE_CONFIG['{platform}']['id']")
        print(f"  ℹ️ Link será enviado sem afiliação (você não ganhará comissão)")
        return original_link
    
    # Cria o link de afiliado conforme a plataforma
    try:
        if platform == 'mercadolivre':
            # Mercado Livre usa link único de afiliado
            # Você deve substituir pelo SEU link de afiliado
            affiliate_link = config['format']
            print(f"  💰 Link de afiliado Mercado Livre aplicado!")
            return affiliate_link
            
        elif platform == 'amazon':
            # Amazon adiciona tag no final da URL
            separator = '&' if '?' in original_link else '?'
            affiliate_link = f"{original_link}{separator}{config['format'].replace('{affiliate_id}', affiliate_id)}"
            print(f"  💰 Link de afiliado Amazon aplicado!")
            return affiliate_link
            
        elif platform == 'shopee':
            # Shopee usa link encurtado (você precisa gerar no painel)
            print(f"  ⚠️ Shopee requer link encurtado do painel de afiliados")
            print(f"  ℹ️ Link será enviado sem afiliação")
            return original_link
            
        elif platform == 'aliexpress':
            # AliExpress usa link de redirecionamento
            affiliate_link = config['format'].replace('{affiliate_id}', affiliate_id)
            print(f"  💰 Link de afiliado AliExpress aplicado!")
            return affiliate_link
            
        elif platform in ['magalu', 'americanas', 'shein']:
            # Essas plataformas adicionam parâmetro na URL
            separator = '&' if '?' in original_link else '?'
            affiliate_link = f"{original_link}{separator}{config['format'].replace('{affiliate_id}', affiliate_id)}"
            print(f"  💰 Link de afiliado {platform} aplicado!")
            return affiliate_link
            
        else:
            print(f"  ⚠️ Formato de afiliado não implementado para '{platform}'")
            return original_link
            
    except Exception as e:
        print(f"  ❌ Erro ao criar link de afiliado: {e}")
        return original_link
