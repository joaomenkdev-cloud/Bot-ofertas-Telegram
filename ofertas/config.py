"""Configurações do bot: Telegram, afiliados, banco, filtros e sites."""

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
