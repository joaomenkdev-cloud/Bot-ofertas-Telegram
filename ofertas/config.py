"""Configurações do bot: Telegram, afiliados, banco, filtros e sites."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Lê as variáveis do arquivo .env (copie o .env.example e preencha)
load_dotenv(BASE_DIR / ".env")

# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 1: CONFIGURAÇÃO DO BOT DO TELEGRAM
# ═════════════════════════════════════════════════════════════════════════════
# Os valores ficam no arquivo .env, que não vai para o git.
# Nunca escreva o token direto no código.

# Token do bot: fale com @BotFather no Telegram e use /newbot
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# ID do seu grupo/canal do Telegram
# Como descobrir? Adicione o bot @userinfobot no seu grupo
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID", "").strip()

# IDs numéricos de quem pode usar /buscar, /status e /config, separados por
# vírgula. Descubra o seu mandando qualquer mensagem para o @userinfobot.
ADMIN_IDS = {
    int(user_id)
    for user_id in os.getenv("ADMIN_IDS", "").replace(" ", "").split(",")
    if user_id.lstrip("-").isdigit()
}

# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 2: CONFIGURAÇÃO DOS LINKS DE AFILIADO
# ═════════════════════════════════════════════════════════════════════════════
# Opcional. Sem afiliado configurado, o bot envia o link normal do produto
# (a oferta sai do mesmo jeito, só não gera comissão).
#
# Os parâmetros ficam no .env e são acrescentados ao link de cada produto.
#
# MERCADO LIVRE (https://afiliados.mercadolivre.com.br/)
#   Gere um link em Ferramentas > Gerador de link, abra o link e copie os
#   parâmetros de rastreamento da URL final (ex.: matt_tool=...&matt_word=...)
#   para ML_AFFILIATE_PARAMS. Confira numa aba anônima se a comissão é
#   atribuída antes de confiar no formato.
#
# AMAZON (https://associados.amazon.com.br/)
#   AMAZON_AFFILIATE_TAG=seu-id-20  vira  ?tag=seu-id-20

_amazon_tag = os.getenv("AMAZON_AFFILIATE_TAG", "").strip()

AFFILIATE_CONFIG = {
    "mercadolivre": {"params": os.getenv("ML_AFFILIATE_PARAMS", "").strip()},
    "amazon": {"params": f"tag={_amazon_tag}" if _amazon_tag else ""},
}

# ═════════════════════════════════════════════════════════════════════════════
# SEÇÃO 3: CONFIGURAÇÃO DO BANCO DE DADOS
# ═════════════════════════════════════════════════════════════════════════════
# O bot usa um arquivo SQLite para salvar quais ofertas já foram enviadas
# e a fila de envio. O arquivo é criado automaticamente na primeira execução.

DB_PATH = Path(os.getenv("DB_PATH") or BASE_DIR / "ofertas.db")

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
