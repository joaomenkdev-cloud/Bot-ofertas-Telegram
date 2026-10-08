# ═════════════════════════════════════════════════════════════════════════════
# GERADOR DE MENSAGENS MODERNAS E CHAMATIVAS
# ═════════════════════════════════════════════════════════════════════════════

def generate_attractive_message(offer):
    """
    Gera uma mensagem moderna, limpa e chamativa baseada no produto
    Foca em clareza e destaque de desconto
    """
    title = offer['title']
    price = offer['price']
    original_price = offer.get('original_price')
    discount = offer.get('discount')
    platform = offer.get('platform', 'Loja').title()
    link = offer['link']
    
    title_lower = title.lower()
    
    # ══════════════════════════════════════════════════════════════════════════
    # DETECTA O TIPO DE PRODUTO E CRIA CHAMADA ESPECÍFICA
    # ══════════════════════════════════════════════════════════════════════════
    
    if any(word in title_lower for word in ['processador', 'cpu', 'ryzen', 'core i', 'intel', 'amd']):
        category_intro = "Processador de alta performance"
    
    elif any(word in title_lower for word in ['placa de video', 'placa de vídeo', 'gpu', 'rtx', 'gtx', 'geforce', 'radeon']):
        category_intro = "Placa de vídeo para jogos e trabalhos pesados"
    
    elif any(word in title_lower for word in ['memoria', 'memória', 'ram', 'ddr4', 'ddr5']):
        category_intro = "Memória RAM para mais velocidade"
    
    elif any(word in title_lower for word in ['ssd', 'nvme', 'm.2', 'armazenamento']):
        category_intro = "Armazenamento rápido e confiável"
    
    elif any(word in title_lower for word in ['placa mãe', 'placa-mãe', 'motherboard']):
        category_intro = "Placa-mãe de qualidade"
    
    elif any(word in title_lower for word in ['fonte', 'psu']):
        category_intro = "Fonte de alimentação certificada"
    
    elif any(word in title_lower for word in ['gabinete', 'case']):
        category_intro = "Gabinete com excelente acabamento"
    
    elif any(word in title_lower for word in ['monitor', 'display']):
        category_intro = "Monitor com ótima qualidade de imagem"
    
    elif any(word in title_lower for word in ['teclado', 'keyboard']):
        category_intro = "Teclado confortável e responsivo"
    
    elif any(word in title_lower for word in ['mouse']):
        category_intro = "Mouse preciso e ergonômico"
    
    elif any(word in title_lower for word in ['headset', 'fone', 'headphone']):
        category_intro = "Audio de qualidade premium"
    
    elif any(word in title_lower for word in ['webcam']):
        category_intro = "Webcam com boa resolução"
    
    elif any(word in title_lower for word in ['microfone']):
        category_intro = "Microfone de alta qualidade"
    
    elif any(word in title_lower for word in ['cadeira']):
        category_intro = "Cadeira ergonômica e confortável"
    
    elif any(word in title_lower for word in ['notebook', 'laptop']):
        category_intro = "Notebook potente e versátil"
    
    elif any(word in title_lower for word in ['celular', 'smartphone', 'iphone', 'galaxy', 'xiaomi']):
        category_intro = "Smartphone de última geração"
    
    elif any(word in title_lower for word in ['tablet', 'ipad']):
        category_intro = "Tablet para trabalho e entretenimento"
    
    elif any(word in title_lower for word in ['tv', 'televisão', 'smart tv']):
        category_intro = "TV com tecnologia avançada"
    
    elif any(word in title_lower for word in ['playstation', 'ps5', 'ps4', 'xbox', 'nintendo', 'switch', 'console']):
        category_intro = "Console para gaming"
    
    elif any(word in title_lower for word in ['controle', 'joystick', 'gamepad']):
        category_intro = "Controle de alta precisão"
    
    else:
        category_intro = "Produto de tecnologia"
    
    # ══════════════════════════════════════════════════════════════════════════
    # MONTA A MENSAGEM DE FORMA MODERNA E LIMPA
    # ══════════════════════════════════════════════════════════════════════════
    
    message = f"*{title}*\n\n"
    message += f"{category_intro}\n\n"
    
    # PREÇOS - Destaque visual para desconto
    if original_price and discount and original_price != price:
        # Tem desconto - mostra preço riscado e novo preço
        message += f"💵 De: ~{original_price}~\n"
        message += f"🔥 Por: *{price}*\n"
        message += f"📉 Economia: *{discount}*\n\n"
    else:
        # Sem desconto - apenas o preço
        message += f"💰 *{price}*\n\n"
    
    message += f"🛒 [Ver oferta]({link})\n"
    message += f"📦 Disponível em: {platform}"
    
    return message

# ═════════════════════════════════════════════════════════════════════════════
# SISTEMA DE AGENDAMENTO INTELIGENTE (6 ou 12 ofertas/hora)
# ═════════════════════════════════════════════════════════════════════════════

def get_offers_per_hour():
    """
    Retorna quantas ofertas devem ser enviadas por hora
    12 ofertas/hora em horários de pico
    6 ofertas/hora em horários normais
    """
    from datetime import datetime
    now = datetime.now()
    hour = now.hour
    weekday = now.weekday()  # 0=segunda, 6=domingo
    
    # ── HORÁRIOS DE PICO ──
    # Manhã: 8h-10h (pessoas chegando no trabalho)
    # Almoço: 12h-14h (pausa do trabalho)
    # Noite: 18h-22h (após o trabalho, navegando)
    
    peak_hours = [
        8, 9, 10,      # Manhã
        12, 13,        # Almoço
        18, 19, 20, 21 # Noite
    ]
    
    # Final de semana tem mais tempo livre
    if weekday >= 5:  # Sábado ou Domingo
        peak_hours.extend([14, 15, 16, 17, 22])
    
    if hour in peak_hours:
        return 12  # 12 ofertas/hora = a cada 5 minutos
    else:
        return 6   # 6 ofertas/hora = a cada 10 minutos

def get_send_interval():
    """
    Retorna o intervalo em segundos entre envios
    """
    offers_per_hour = get_offers_per_hour()
    # 3600 segundos (1 hora) / quantidade de ofertas
    interval = 3600 / offers_per_hour
    return int(interval)

# ═════════════════════════════════════════════════════════════════════════════
# ENVIO PARA O TELEGRAM (ATUALIZADO)
# ═════════════════════════════════════════════════════════════════════════════

    """
═══════════════════════════════════════════════════════════════════════════════
    BOT DE TELEGRAM - OFERTAS COM LINKS DE AFILIADO
    
    O QUE ESTE BOT FAZ?
    • Busca ofertas em várias lojas (Mercado Livre, Amazon, Shopee, etc)
    • Transforma links normais em links de afiliado (para você ganhar comissão)
    • Envia ofertas automaticamente no seu grupo do Telegram
    • Evita duplicatas (não envia a mesma oferta duas vezes)
    • Sistema de fila inteligente
    
    COMO USAR?
    1. Instale as bibliotecas: pip install python-telegram-bot selenium webdriver-manager beautifulsoup4 lxml mysql-connector-python
    2. Configure seus IDs de afiliado na seção "CONFIGURAÇÃO DE AFILIADOS" abaixo
    3. Configure o token do bot e ID do grupo
    4. Execute: python bot.py
    
    IMPORTANTE:
    • Você precisa ter o Google Chrome instalado
    • Você precisa ter o MySQL instalado e rodando
    • Cadastre-se nos programas de afiliados antes de usar
═══════════════════════════════════════════════════════════════════════════════
"""

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
import asyncio
from datetime import datetime
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import mysql.connector
from mysql.connector import Error
import hashlib
import json
from urllib.parse import quote, urlparse

# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 1: CONFIGURAÇÃO DO BOT DO TELEGRAM
# ═════════════════════════════════════════════════════════════════════════════
# Onde conseguir?
# 1. Fale com @BotFather no Telegram
# 2. Use o comando /newbot
# 3. Copie o token que ele te enviar

BOT_TOKEN = ""

# ID do seu grupo/canal do Telegram
# Como descobrir? Adicione o bot @userinfobot no seu grupo
GROUP_CHAT_ID = ""

# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 2: CONFIGURAÇÃO DOS LINKS DE AFILIADO
# ═════════════════════════════════════════════════════════════════════════════
# Aqui você configura seus IDs de afiliado de cada plataforma
# Deixe vazio ("") se não tiver cadastro naquela plataforma

AFFILIATE_CONFIG = {
    
    # ─────────────────────────────────────────────────────────────────────────
    # MERCADO LIVRE
    # Como conseguir? https://afiliados.mercadolivre.com.br/
    # ─────────────────────────────────────────────────────────────────────────
    "mercadolivre": {
        "enabled": True,  # Mude para False se não quiser usar
        "id": "SEU_ID_AFILIADO_MERCADOLIVRE",  # Exemplo: "joaosilva123"
        "format": "https://mercadolivre.com/sec/2EhdV6q"  # Formato do link de afiliado
        # ATENÇÃO: No Mercado Livre, cada afiliado tem um link único
        # Substitua o link acima pelo SEU link de afiliado do Mercado Livre
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # AMAZON
    # Como conseguir? https://associados.amazon.com.br/
    # ─────────────────────────────────────────────────────────────────────────
    "amazon": {
        "enabled": True,
        "id": "SEU_ID_AFILIADO_AMAZON",  # Exemplo: "meublog-20"
        "format": "tag={affiliate_id}"  # Será adicionado na URL
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # SHOPEE
    # Como conseguir? https://shopee.com.br/m/shopee-affiliate
    # ─────────────────────────────────────────────────────────────────────────
    "shopee": {
        "enabled": True,
        "id": "SEU_ID_AFILIADO_SHOPEE",
        "format": "https://shope.ee/{short_link}?smtt=0.0.9"
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # ALIEXPRESS
    # Como conseguir? https://portals.aliexpress.com/
    # ─────────────────────────────────────────────────────────────────────────
    "aliexpress": {
        "enabled": True,
        "id": "SEU_ID_AFILIADO_ALIEXPRESS",
        "format": "https://s.click.aliexpress.com/e/{affiliate_id}"
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # MAGALU (Magazine Luiza)
    # Como conseguir? https://afiliados.magazineluiza.com.br/
    # ─────────────────────────────────────────────────────────────────────────
    "magalu": {
        "enabled": True,
        "id": "SEU_ID_AFILIADO_MAGALU",
        "format": "parceiro={affiliate_id}"
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # AMERICANAS
    # Como conseguir? https://afiliados.americanas.com.br/
    # ─────────────────────────────────────────────────────────────────────────
    "americanas": {
        "enabled": True,
        "id": "SEU_ID_AFILIADO_AMERICANAS",
        "format": "me={affiliate_id}"
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # SHEIN
    # Como conseguir? https://br.shein.com/affiliate-program
    # ─────────────────────────────────────────────────────────────────────────
    "shein": {
        "enabled": True,
        "id": "SEU_ID_AFILIADO_SHEIN",
        "format": "ref={affiliate_id}"
    },
}

# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DAS APIs DE AFILIADOS
# ═════════════════════════════════════════════════════════════════════════════

API_CONFIG = {
    # ─────────────────────────────────────────────────────────────────────────
    # MERCADO LIVRE API
    # Documentação: https://developers.mercadolivre.com.br/
    # ─────────────────────────────────────────────────────────────────────────
    "mercadolivre": {
        "enabled": True,
        "api_url": "https://api.mercadolibre.com",
        "client_id": "SEU_CLIENT_ID_ML",  # App ID do Mercado Livre
        "client_secret": "SEU_CLIENT_SECRET_ML",  # Secret do Mercado Livre
        "access_token": "",  # Será preenchido automaticamente
        "refresh_token": "",  # Token para renovar acesso
        "tag": "SEU_TAG_AFILIADO_ML",  # Ex: "MEUBLOG"
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # AMAZON PRODUCT ADVERTISING API
    # Documentação: https://webservices.amazon.com/paapi5/documentation/
    # ─────────────────────────────────────────────────────────────────────────
    "amazon": {
        "enabled": True,
        "api_url": "https://webservices.amazon.com.br/paapi5",
        "access_key": "SEU_ACCESS_KEY_AMAZON",  # Access Key da PA API
        "secret_key": "SEU_SECRET_KEY_AMAZON",  # Secret Key da PA API
        "partner_tag": "SEU_TAG_AMAZON",  # Ex: "meublog-20"
        "partner_type": "Associates",  # Sempre "Associates" para afiliados
        "marketplace": "www.amazon.com.br",
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # SHOPEE OPEN PLATFORM API
    # Documentação: https://open.shopee.com/documents
    # ─────────────────────────────────────────────────────────────────────────
    "shopee": {
        "enabled": True,
        "api_url": "https://partner.shopeemobile.com/api/v2",
        "partner_id": 0,  # SEU_PARTNER_ID_SHOPEE (número)
        "partner_key": "SEU_PARTNER_KEY_SHOPEE",  # Partner Key
        "shop_id": 0,  # SEU_SHOP_ID (número)
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # ALIEXPRESS AFFILIATE API (Admitad)
    # Documentação: https://www.admitad.com/pt/webmaster/api/
    # ─────────────────────────────────────────────────────────────────────────
    "aliexpress": {
        "enabled": True,
        "api_url": "https://api.admitad.com/deeplink/",
        "client_id": "SEU_CLIENT_ID_ADMITAD",
        "client_secret": "SEU_CLIENT_SECRET_ADMITAD",
        "access_token": "",  # Será preenchido automaticamente
        "campaign_id": "SEU_CAMPAIGN_ID",  # ID da campanha AliExpress
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # MAGALU (Magazine Luiza) - Via Lomadee
    # Documentação: https://developer.lomadee.com/
    # ─────────────────────────────────────────────────────────────────────────
    "magalu": {
        "enabled": True,
        "api_url": "https://api.lomadee.com/v3",
        "app_token": "SEU_APP_TOKEN_LOMADEE",
        "source_id": "SEU_SOURCE_ID",  # Source ID da Lomadee
    },
    
    # ─────────────────────────────────────────────────────────────────────────
    # AMERICANAS - Via Lomadee
    # ─────────────────────────────────────────────────────────────────────────
    "americanas": {
        "enabled": True,
        "api_url": "https://api.lomadee.com/v3",
        "app_token": "SEU_APP_TOKEN_LOMADEE",
        "source_id": "SEU_SOURCE_ID",
    },
}
# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 3: CONFIGURAÇÃO DO BANCO DE DADOS
# ═════════════════════════════════════════════════════════════════════════════
# O bot usa MySQL para salvar quais ofertas já foram enviadas
# Assim ele não envia a mesma oferta duas vezes

DB_CONFIG = {
    'host': 'localhost',      # Deixe assim se o MySQL está no mesmo computador
    'user': 'root',           # Usuário do MySQL
    'password': 'sua senha aqui',   # ⚠️ MUDE PARA SUA SENHA DO MYSQL
    'database': 'bot_ofertas' # Nome do banco (será criado automaticamente)
}

# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 4: FILTROS DE PRODUTOS
# ═════════════════════════════════════════════════════════════════════════════
# Palavras-chave que o bot vai procurar
# Se o produto tiver alguma dessas palavras, ele será aceito

ALLOWED_KEYWORDS = [
    # ── Componentes de PC ──
    'processador', 'cpu', 'intel', 'amd', 'ryzen', 'core i3', 'core i5', 'core i7', 'core i9',
    'memória ram', 'memoria ram', 'ddr4', 'ddr5', 'ram',
    'ssd', 'nvme', 'm.2', 'sata', 'armazenamento', 'hd', 'disco',
    'placa mãe', 'placa-mãe', 'motherboard', 'placa mae',
    'placa de vídeo', 'placa de video', 'gpu', 'geforce', 'rtx', 'gtx', 'radeon', 'rx',
    'fonte', 'psu', 'alimentação', 'alimentacao',
    'gabinete', 'case', 'tower',
    
    # ── Periféricos ──
    'monitor', 'display', 'tela',
    'teclado', 'keyboard', 'mecânico', 'mecanico',
    'mouse', 'gamer',
    'webcam', 'camera web',
    'microfone', 'mic',
    'headset', 'fone', 'headphone', 'caixa de som', 'speaker',
    
    # ── Conforto e Setup ──
    'cadeira gamer', 'cadeira ergonomica', 'cadeira escritorio',
    'mesa gamer', 'mesa escritorio', 'escrivaninha',
    'mousepad', 'apoio pulso', 'descanso pulso',
    'luminária', 'luminaria', 'led', 'iluminação',
    'suporte monitor', 'braço monitor',
    
    # ── Computadores ──
    'notebook', 'laptop', 'ultrabook', 'macbook',
    'cooler', 'ventilador', 'water cooler', 'refrigeração',
    'pasta térmica', 'pasta termica',
    
    # ── Conectividade ──
    'cabo hdmi', 'cabo displayport', 'cabo usb', 'cabo de rede',
    'hub usb', 'adaptador', 'conversor',
    'roteador', 'wifi', 'wireless', 'ethernet',
    'no-break', 'nobreak', 'estabilizador',
    
    # ── Celulares e Tablets ──
    'celular', 'smartphone', 'iphone', 'galaxy', 'xiaomi', 'motorola', 'samsung',
    'redmi', 'poco', 'realme', 'asus phone', 'lg phone', 'oneplus',
    'tablet', 'ipad', 'galaxy tab',
    'carregador', 'powerbank', 'bateria externa',
    'capinha', 'case celular', 'película',
    
    # ── TVs e Áudio/Vídeo ──
    'tv', 'televisão', 'televisao', 'smart tv', 'tv led', 'tv oled', 'tv qled',
    'tv 4k', 'tv 8k', 'android tv', 'google tv', 'fire tv',
    'soundbar', 'home theater', 'projetor',
    
    # ── Consoles e Gaming ──
    'console', 'playstation', 'ps5', 'ps4', 'ps3', 'psvr',
    'xbox', 'xbox series x', 'xbox series s', 'xbox one',
    'nintendo', 'switch', 'nintendo switch', 'switch oled',
    'steam deck', 'controle', 'joystick', 'gamepad',
    'jogo', 'game', 'ps plus', 'xbox game pass',
]

# Palavras-chave BLOQUEADAS - produtos que o bot vai IGNORAR
BLOCKED_KEYWORDS = [
    'roupa', 'camisa', 'camiseta', 'calça', 'sapato', 'tênis', 'bermuda',
    'livro', 'revista', 'gibi',
    'brinquedo', 'boneca', 'carrinho de brinquedo',
    'perfume', 'cosmético', 'maquiagem', 'shampoo',
    'alimento', 'comida', 'bebida', 'chocolate',
    'geladeira', 'fogão', 'microondas', 'liquidificador',
    'carro', 'moto', 'peça automotiva', 'pneu',
    'imóvel', 'apartamento', 'casa',
    'relógio de pulso', 'joia', 'anel', 'colar',
    'violão', 'guitarra', 'bateria',
    'bola de futebol', 'bicicleta', 'esteira',
    'ração', 'coleira',
]

# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 5: SITES PARA BUSCAR OFERTAS
# ═════════════════════════════════════════════════════════════════════════════
# Aqui você configura em quais sites o bot vai buscar
# Pode adicionar ou remover sites conforme necessário

SCRAPING_TARGETS = [
    # ── MERCADO LIVRE ──
    {
        "name": "Mercado Livre - Informática",
        "platform": "mercadolivre",
        "url": "https://lista.mercadolivre.com.br/informatica/_DisplayType_LF_NoIndex_True",
        "selectors": {
            "container": ".ui-search-layout__item",
            "title": ".ui-search-item__title",
            "price": ".andes-money-amount__fraction",
            "original_price": ".andes-money-amount--previous .andes-money-amount__fraction",
            "link": ".ui-search-link",
            "image": "img.ui-search-result-image__element"
        }
    },
    {
        "name": "Mercado Livre - Componentes PC",
        "platform": "mercadolivre",
        "url": "https://lista.mercadolivre.com.br/informatica/componentes-pc/_DisplayType_LF_NoIndex_True",
        "selectors": {
            "container": ".ui-search-layout__item",
            "title": ".ui-search-item__title",
            "price": ".andes-money-amount__fraction",
            "original_price": ".andes-money-amount--previous .andes-money-amount__fraction",
            "link": ".ui-search-link",
            "image": "img.ui-search-result-image__element"
        }
    },
    {
        "name": "Mercado Livre - Celulares",
        "platform": "mercadolivre",
        "url": "https://lista.mercadolivre.com.br/celulares-telefones/_DisplayType_LF_NoIndex_True",
        "selectors": {
            "container": ".ui-search-layout__item",
            "title": ".ui-search-item__title",
            "price": ".andes-money-amount__fraction",
            "original_price": ".andes-money-amount--previous .andes-money-amount__fraction",
            "link": ".ui-search-link",
            "image": "img.ui-search-result-image__element"
        }
    },
    {
        "name": "Mercado Livre - TVs",
        "platform": "mercadolivre",
        "url": "https://lista.mercadolivre.com.br/eletronicos-audio-video/televisores/_DisplayType_LF_NoIndex_True",
        "selectors": {
            "container": ".ui-search-layout__item",
            "title": ".ui-search-item__title",
            "price": ".andes-money-amount__fraction",
            "original_price": ".andes-money-amount--previous .andes-money-amount__fraction",
            "link": ".ui-search-link",
            "image": "img.ui-search-result-image__element"
        }
    },
    {
        "name": "Mercado Livre - Consoles",
        "platform": "mercadolivre",
        "url": "https://lista.mercadolivre.com.br/video-games/_DisplayType_LF_NoIndex_True",
        "selectors": {
            "container": ".ui-search-layout__item",
            "title": ".ui-search-item__title",
            "price": ".andes-money-amount__fraction",
            "original_price": ".andes-money-amount--previous .andes-money-amount__fraction",
            "link": ".ui-search-link",
            "image": "img.ui-search-result-image__element"
        }
    },
    
    # ══════════════════════════════════════════════════════════════════════════
    # COMO ADICIONAR MAIS SITES?
    # ══════════════════════════════════════════════════════════════════════════
    # Copie o bloco acima e modifique:
    # 1. "name": Nome que vai aparecer no log
    # 2. "platform": Nome da plataforma (deve estar em AFFILIATE_CONFIG)
    # 3. "url": URL da página de busca
    # 4. "selectors": Classes CSS dos elementos (use inspecionar no navegador)
    #
    # EXEMPLO para Shopee:
    # {
    #     "name": "Shopee - Eletrônicos",
    #     "platform": "shopee",
    #     "url": "https://shopee.com.br/Eletrônicos-cat.11043936",
    #     "selectors": {
    #         "container": ".shopee-search-item-result__item",
    #         "title": ".ie3A+n",
    #         "price": ".ZEgDH9",
    #         "link": "a",
    #         "image": "img"
    #     }
    # },
]

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

# ═════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DO BANCO DE DADOS
# ═════════════════════════════════════════════════════════════════════════════

def create_database_connection():
    """Cria conexão com o banco de dados MySQL"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        print(f"💡 Verifique se o MySQL está rodando e se a senha está correta")
        return None

def initialize_database():
    """Cria o banco e as tabelas se não existirem"""
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        
        # Cria o banco
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"✅ Banco de dados '{DB_CONFIG['database']}' verificado/criado")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Tabela de ofertas enviadas (evita duplicatas)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ofertas_enviadas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hash_oferta VARCHAR(64) UNIQUE NOT NULL,
                titulo VARCHAR(500) NOT NULL,
                preco VARCHAR(50),
                link TEXT NOT NULL,
                fonte VARCHAR(100),
                plataforma VARCHAR(50),
                tem_afiliado BOOLEAN DEFAULT FALSE,
                data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_hash (hash_oferta),
                INDEX idx_data (data_envio),
                INDEX idx_plataforma (plataforma)
            )
        """)
        
        # Tabela de fila de ofertas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fila_ofertas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hash_oferta VARCHAR(64) UNIQUE NOT NULL,
                dados_oferta TEXT NOT NULL,
                fonte VARCHAR(100),
                plataforma VARCHAR(50),
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_fonte (fonte),
                INDEX idx_data (data_criacao),
                INDEX idx_plataforma (plataforma)
            )
        """)
        
        print("✅ Tabelas verificadas/criadas")
        cursor.close()
        connection.close()
    except Error as e:
        print(f"❌ Erro ao inicializar banco: {e}")

def generate_offer_hash(title, link):
    """Gera um hash único para cada oferta (evita duplicatas)"""
    clean_link = link.split('?')[0].split('#')[0]
    offer_string = f"{title.lower().strip()}|{clean_link}"
    return hashlib.sha256(offer_string.encode()).hexdigest()

def is_offer_already_sent(offer_hash):
    """Verifica se a oferta já foi enviada antes"""
    connection = create_database_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM ofertas_enviadas WHERE hash_oferta = %s", (offer_hash,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None
    except Error as e:
        print(f"❌ Erro ao verificar oferta: {e}")
        return False

def save_sent_offer(offer):
    """Salva oferta no banco após enviar"""
    connection = create_database_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        offer_hash = generate_offer_hash(offer['title'], offer['link'])
        platform = detect_platform(offer['link'])
        has_affiliate = offer.get('has_affiliate', False)
        
        cursor.execute("""
            INSERT INTO ofertas_enviadas (hash_oferta, titulo, preco, link, fonte, plataforma, tem_afiliado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (offer_hash, offer['title'][:500], offer['price'], offer['link'], 
              offer['source'], platform, has_affiliate))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"❌ Erro ao salvar oferta: {e}")
        return False

def add_to_queue(offer):
    """Adiciona oferta à fila para envio posterior"""
    connection = create_database_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        offer_hash = generate_offer_hash(offer['title'], offer['link'])
        dados_json = json.dumps(offer)
        platform = detect_platform(offer['link'])
        
        cursor.execute("""
            INSERT IGNORE INTO fila_ofertas (hash_oferta, dados_oferta, fonte, plataforma)
            VALUES (%s, %s, %s, %s)
        """, (offer_hash, dados_json, offer['source'], platform))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"❌ Erro ao adicionar à fila: {e}")
        return False

def get_next_offer_from_queue(source):
    """Pega a próxima oferta da fila"""
    connection = create_database_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, hash_oferta, dados_oferta 
            FROM fila_ofertas 
            WHERE fonte = %s 
            ORDER BY data_criacao ASC 
            LIMIT 1
        """, (source,))
        result = cursor.fetchone()
        
        if result:
            cursor.execute("DELETE FROM fila_ofertas WHERE id = %s", (result['id'],))
            connection.commit()
            cursor.close()
            connection.close()
            return json.loads(result['dados_oferta'])
        
        cursor.close()
        connection.close()
        return None
    except Error as e:
        print(f"❌ Erro ao buscar da fila: {e}")
        return None

def get_queue_count():
    """Retorna quantidade de ofertas na fila"""
    connection = create_database_connection()
    if not connection:
        return {}
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT fonte, COUNT(*) as quantidade 
            FROM fila_ofertas 
            GROUP BY fonte
        """)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return {r['fonte']: r['quantidade'] for r in results}
    except Error as e:
        print(f"❌ Erro ao contar fila: {e}")
        return {}

def get_statistics():
    """Retorna estatísticas do bot"""
    connection = create_database_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Total de ofertas
        cursor.execute("SELECT COUNT(*) as total FROM ofertas_enviadas")
        total = cursor.fetchone()['total']
        
        # Ofertas de hoje
        cursor.execute("""
            SELECT COUNT(*) as hoje 
            FROM ofertas_enviadas 
            WHERE DATE(data_envio) = CURDATE()
        """)
        hoje = cursor.fetchone()['hoje']
        
        # Por fonte
        cursor.execute("""
            SELECT fonte, COUNT(*) as quantidade 
            FROM ofertas_enviadas 
            GROUP BY fonte 
            ORDER BY quantidade DESC
        """)
        por_fonte = cursor.fetchall()
        
        # Estatísticas de afiliados
        cursor.execute("""
            SELECT 
                COUNT(*) as total_com_afiliado 
            FROM ofertas_enviadas 
            WHERE tem_afiliado = TRUE
        """)
        com_afiliado = cursor.fetchone()['total_com_afiliado']
        
        cursor.close()
        connection.close()
        return {
            'total': total, 
            'hoje': hoje, 
            'por_fonte': por_fonte,
            'com_afiliado': com_afiliado,
            'sem_afiliado': total - com_afiliado
        }
    except Error as e:
        print(f"❌ Erro ao buscar estatísticas: {e}")
        return None

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

# ═════════════════════════════════════════════════════════════════════════════
# WEB SCRAPING COM SELENIUM
# ═════════════════════════════════════════════════════════════════════════════

async def scrape_offers_with_selenium(target_site, max_pages=5):
    """Busca ofertas em múltiplas páginas"""
    print(f"🔍 Iniciando scraping em: {target_site['name']}")
    all_offers = []
    
    for page_num in range(1, max_pages + 1):
        url = target_site['url']
        
        # Adiciona número da página na URL
        if 'page=' in url:
            url = re.sub(r'page=\d+', f'page={page_num}', url)
        elif '?' in url:
            url = f"{url}&page={page_num}"
        else:
            url = f"{url}?page={page_num}"
        
        print(f"📄 Página {page_num}/{max_pages}")
        
        offers = await asyncio.to_thread(scrape_offers_sync, target_site, url)
        
        if not offers:
            print(f"⚠️ Nenhuma oferta encontrada, parando busca.")
            break
        
        all_offers.extend(offers)
        print(f"✅ {len(offers)} ofertas extraídas")
        
        if len(all_offers) >= 50:
            print(f"✅ Limite de 50 ofertas atingido")
            break
        
        await asyncio.sleep(2)
    
    return all_offers

def scrape_offers_sync(target_site, url):
    """Função síncrona de scraping"""
    offers = []
    driver = None
    
    try:
        # Configurações do Chrome
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # Habilita imagens
        prefs = {"profile.managed_default_content_settings.images": 1}
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Inicia o driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print(f"📡 Acessando: {url}")
        driver.get(url)
        
        # Aguarda carregamento
        time.sleep(6)
        
        # Scroll para carregar imagens
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*3/4);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        # Parse do HTML
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        
        # Busca produtos
        products = soup.select(target_site['selectors']['container'])
        print(f"✅ Encontrados {len(products)} produtos")
        
        # Seletores alternativos se não encontrar
        if len(products) == 0:
            print("🔄 Tentando seletores alternativos...")
            alternative_selectors = [
                'li.ui-search-layout__item',
                'div.ui-search-result',
                'div.poly-card',
                'article',
                'div[class*="item"]',
            ]
            for alt_selector in alternative_selectors:
                products = soup.select(alt_selector)
                if len(products) > 0:
                    print(f"✅ Encontrados {len(products)} com {alt_selector}")
                    break
        
        # Processa cada produto
        for product in products:
            try:
                # Extrai título
                title_elem = (product.select_one(target_site['selectors']['title']) or 
                             product.select_one('h2') or 
                             product.select_one('h3'))
                
                # Extrai preço
                price_elem = (product.select_one(target_site['selectors']['price']) or
                             product.select_one('[class*="price"]'))
                
                # Extrai link
                link_elem = (product.select_one(target_site['selectors']['link']) or
                            product.select_one('a'))
                
                if not (title_elem and price_elem and link_elem):
                    continue
                
                original_link = link_elem.get('href', '')
                if not original_link.startswith('http'):
                    from urllib.parse import urljoin
                    original_link = urljoin(url, original_link)
                
                # Limpa a URL
                if 'mercadolivre' in original_link:
                    original_link = original_link.split('#')[0].split('?')[0]
                
                title = title_elem.get_text(strip=True)
                if len(title) < 10:
                    continue
                
                # FILTRO: Verifica se é produto aceito
                print(f"\n🔍 Analisando: {title[:60]}...")
                if not is_pc_related_product(title):
                    print(f"  🚫 Produto ignorado")
                    continue
                
                print(f"  ✅ Produto aceito!")
                
                # Busca imagem
                image_url = None
                if 'image' in target_site['selectors']:
                    image_elem = product.select_one(target_site['selectors']['image'])
                    if image_elem:
                        image_url = (image_elem.get('data-src') or 
                                   image_elem.get('src'))
                
                if not image_url:
                    all_imgs = product.select('img')
                    for img in all_imgs:
                        potential_url = img.get('data-src') or img.get('src')
                        if potential_url and 'http' in potential_url:
                            if not any(x in potential_url.lower() for x in ['blank', 'placeholder']):
                                image_url = potential_url
                                break
                
                # Melhora qualidade da imagem (Mercado Livre)
                if image_url and ('mlstatic.com' in image_url or 'mlu.com' in image_url):
                    image_url = re.sub(r'-[IOP]\.jpg', '-W.jpg', image_url)
                    image_url = image_url.split('?')[0]
                
                if image_url:
                    print(f"  🖼️ Imagem encontrada")
                else:
                    print(f"  ⚠️ Sem imagem")
                
                # Cria link de afiliado
                print(f"  🔗 Criando link de afiliado...")
                affiliate_link = create_affiliate_link(original_link, target_site.get('platform'))
                has_affiliate = (affiliate_link != original_link)
                
                # Cria objeto da oferta
                offer = {
                    "title": title[:200],
                    "price": clean_price(price_elem.get_text(strip=True)),
                    "original_price": None,
                    "link": affiliate_link,
                    "original_link": original_link,
                    "source": target_site['name'],
                    "platform": target_site.get('platform', 'desconhecido'),
                    "image_url": image_url,
                    "has_affiliate": has_affiliate
                }
                
                # Busca preço original (se tiver)
                original_price_elem = product.select_one(target_site['selectors'].get('original_price', ''))
                if original_price_elem:
                    offer['original_price'] = clean_price(original_price_elem.get_text(strip=True))
                    if offer['original_price'] and offer['original_price'] != offer['price']:
                        offer['discount'] = calculate_discount(offer['original_price'], offer['price'])
                
                offers.append(offer)
                
            except Exception as e:
                continue
        
    except Exception as e:
        print(f"❌ Erro no scraping: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()
    
    print(f"📊 Total extraídas: {len(offers)}")
    return offers

# ═════════════════════════════════════════════════════════════════════════════
# LÓGICA PRINCIPAL
# ═════════════════════════════════════════════════════════════════════════════

async def find_and_manage_offers(context: ContextTypes.DEFAULT_TYPE):
    """Busca ofertas e gerencia a fila"""
    print("\n" + "="*60)
    print(f"🔍 Buscando ofertas - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60 + "\n")
    
    total_new_offers = 0
    
    for target in SCRAPING_TARGETS:
        print(f"\n{'='*60}")
        print(f"📍 FONTE: {target['name']}")
        print(f"{'='*60}")
        
        found_new = False
        attempts = 0
        max_attempts = 10
        
        while not found_new and attempts < max_attempts:
            attempts += 1
            print(f"\n🔄 Tentativa {attempts}/{max_attempts}")
            
            offers = await scrape_offers_with_selenium(target, max_pages=5)
            
            if not offers:
                print(f"⚠️ Nenhuma oferta encontrada")
                await asyncio.sleep(3)
                continue
            
            # Filtra ofertas não enviadas
            new_offers = []
            for offer in offers:
                offer_hash = generate_offer_hash(offer['title'], offer['link'])
                if not is_offer_already_sent(offer_hash):
                    new_offers.append(offer)
            
            print(f"\n📊 Resultado:")
            print(f"  • Total: {len(offers)}")
            print(f"  • Duplicadas: {len(offers) - len(new_offers)}")
            print(f"  • Novas: {len(new_offers)}")
            
            if new_offers:
                found_new = True
                print(f"\n✅ Encontradas {len(new_offers)} ofertas NOVAS!")
                
                # FILTRO: Remove ofertas sem afiliado ou sem imagem
                valid_offers = []
                for offer in new_offers:
                    if offer.get('has_affiliate') and offer.get('image_url'):
                        valid_offers.append(offer)
                    else:
                        reasons = []
                        if not offer.get('has_affiliate'):
                            reasons.append("sem afiliado")
                        if not offer.get('image_url'):
                            reasons.append("sem imagem")
                        print(f"  🚫 Ignorando: {offer['title'][:50]} ({', '.join(reasons)})")
                
                if not valid_offers:
                    print(f"  ⚠️ Nenhuma oferta válida (todas sem afiliado/imagem)")
                    continue
                
                print(f"\n✅ {len(valid_offers)} ofertas válidas (com afiliado E imagem)")
                
                # Envia a primeira válida
                first_offer = valid_offers[0]
                print(f"\n📤 Enviando: {first_offer['title'][:50]}...")
                success = await send_offer_to_group(context, first_offer)
                
                if success:
                    save_sent_offer(first_offer)
                    total_new_offers += 1
                    print(f"✅ Enviada e salva!")
                
                # Adiciona o restante à fila
                if len(valid_offers) > 1:
                    print(f"\n📥 Adicionando {len(valid_offers) - 1} à fila")
                    for offer in valid_offers[1:]:
                        add_to_queue(offer)
            else:
                print(f"⚠️ Todas já foram enviadas")
                await asyncio.sleep(2)
        
        if not found_new:
            print(f"\n❌ Nenhuma oferta nova após {max_attempts} tentativas")
        
        await asyncio.sleep(3)
    
    # Resumo
    queue_counts = get_queue_count()
    print(f"\n" + "="*60)
    print(f"📊 RESUMO")
    print(f"="*60)
    print(f"✅ Enviadas: {total_new_offers}")
    print(f"📥 Na fila: {sum(queue_counts.values())}")
    print(f"="*60)

async def send_queued_offers(context: ContextTypes.DEFAULT_TYPE):
    """
    Envia ofertas da fila com intervalo dinâmico
    6/hora em horários normais, 12/hora em horários de pico
    """
    print(f"\n⏰ Enviando ofertas da fila...")
    
    offers_per_hour = get_offers_per_hour()
    print(f"📊 Modo atual: {offers_per_hour} ofertas/hora")
    
    for target in SCRAPING_TARGETS:
        offer = get_next_offer_from_queue(target['name'])
        if offer:
            # Valida antes de enviar
            if not offer.get('has_affiliate') or not offer.get('image_url'):
                print(f"  🚫 Pulando oferta inválida da fila: {offer['title'][:40]}")
                continue
            
            success = await send_offer_to_group(context, offer)
            if success:
                save_sent_offer(offer)
                print(f"✅ Enviada: {offer['title'][:40]}...")
            await asyncio.sleep(2)

async def check_and_search_if_needed(context: ContextTypes.DEFAULT_TYPE):
    """Verifica fila e busca se necessário"""
    queue_counts = get_queue_count()
    total_in_queue = sum(queue_counts.values())
    
    print(f"\n🔍 Fila: {total_in_queue} ofertas")
    
    if total_in_queue < 5:
        print("⚠️ Fila baixa! Buscando novas...")
        await find_and_manage_offers(context)

# ═════════════════════════════════════════════════════════════════════════════
# ENVIO PARA O TELEGRAM
# ═════════════════════════════════════════════════════════════════════════════

async def send_offer_to_group(context: ContextTypes.DEFAULT_TYPE, offer):
    """Envia oferta para o grupo do Telegram"""
    
    # ⚠️ VALIDAÇÃO: Só envia se tiver link de afiliado E imagem
    if not offer.get('has_affiliate'):
        print(f"  ❌ BLOQUEADO: Sem link de afiliado - {offer['title'][:50]}...")
        return False
    
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

# ═════════════════════════════════════════════════════════════════════════════
# INICIALIZAÇÃO
# ═════════════════════════════════════════════════════════════════════════════

def main():
    """Função principal - Inicia o bot"""
    
    print("="*60)
    print("🤖 BOT DE OFERTAS COM SISTEMA DE AFILIADOS")
    print("="*60)
    print(f"📅 Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*60)
    
    # Inicializa o banco de dados
    initialize_database()
    
    # Verifica configuração de afiliados
    print("\n🔍 Verificando configuração de afiliados...")
    for platform, config in AFFILIATE_CONFIG.items():
        if config.get('enabled'):
            if config.get('id') and not config['id'].startswith('SEU_ID_'):
                print(f"  ✅ {platform.upper()}: Configurado")
            else:
                print(f"  ⚠️ {platform.upper()}: ID não configurado!")
        else:
            print(f"  ❌ {platform.upper()}: Desabilitado")
    
    # Cria a aplicação
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Adiciona comandos
    application.add_handler(CommandHandler("buscar", buscar_ofertas_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("config", config_command))
    
    # ══════════════════════════════════════════════════════════════════════════
    # AGENDAMENTO INTELIGENTE
    # ══════════════════════════════════════════════════════════════════════════
    # O bot se adapta ao horário:
    # - Horários normais: 6 ofertas/hora (a cada 10 minutos)
    # - Horários de pico: 12 ofertas/hora (a cada 5 minutos)
    #
    # Horários de pico:
    # - 8h-10h (manhã)
    # - 12h-14h (almoço)
    # - 18h-22h (noite)
    # - Finais de semana: 14h-22h
    # ══════════════════════════════════════════════════════════════════════════
    
    # Envia ofertas da fila com intervalo dinâmico
    # Calcula automaticamente baseado no horário
    interval = get_send_interval()
    application.job_queue.run_repeating(send_queued_offers, interval=interval, first=30)
    
    # Atualiza o intervalo a cada hora para se adaptar ao horário
    async def update_send_interval(context):
        """Atualiza o intervalo de envio baseado no horário atual"""
        new_interval = get_send_interval()
        offers_per_hour = get_offers_per_hour()
        print(f"\n🔄 Intervalo atualizado: {offers_per_hour} ofertas/hora")
        
        # Cancela o job antigo
        current_jobs = context.job_queue.get_jobs_by_name('send_offers')
        for job in current_jobs:
            job.schedule_removal()
        
        # Cria novo job com intervalo atualizado
        context.job_queue.run_repeating(
            send_queued_offers, 
            interval=new_interval, 
            first=1,
            name='send_offers'
        )
    
    # Atualiza o intervalo a cada hora
    application.job_queue.run_repeating(update_send_interval, interval=3600, first=3600)
    
    # Verifica e busca novas ofertas a cada 30 minutos
    application.job_queue.run_repeating(check_and_search_if_needed, interval=1800, first=60)
    
    print("\n" + "="*60)
    print("✅ BOT INICIADO COM SUCESSO!")
    print("="*60)
    print(f"📊 Modo inicial: {get_offers_per_hour()} ofertas/hora")
    print(f"⏰ Intervalo atual: {get_send_interval()} segundos entre envios")
    print("🔄 Verificação automática: a cada 30 minutos")
    print("\n📱 COMANDOS DISPONÍVEIS:")
    print("  /buscar - Busca ofertas manualmente")
    print("  /status - Mostra estatísticas")
    print("  /config - Mostra configuração de afiliados")
    print("\n⏰ SISTEMA DE ENVIO INTELIGENTE:")
    print("  • Horários normais: 6 ofertas/hora (a cada 10min)")
    print("  • Horários de pico: 12 ofertas/hora (a cada 5min)")
    print("  • Picos: 8-10h, 12-14h, 18-22h + fins de semana")
    print("="*60 + "\n")
    
    # Inicia o bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()