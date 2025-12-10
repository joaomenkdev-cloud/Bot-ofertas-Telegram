"""
Bot do Telegram - Web Scraping de Ofertas com Sistema de Fila
Bibliotecas: python-telegram-bot, selenium, webdriver-manager, beautifulsoup4, mysql-connector-python

Instalação necessária:
pip install python-telegram-bot selenium webdriver-manager beautifulsoup4 lxml mysql-connector-python

IMPORTANTE: Certifique-se de ter o Google Chrome instalado no sistema!
IMPORTANTE: Certifique-se de ter o MySQL instalado e rodando!

Para executar:
python bot.py
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

# ==============================================================================
# CONFIGURAÇÃO DO BOT
# ==============================================================================
BOT_TOKEN = ""
GROUP_CHAT_ID = ""

# CONFIGURAÇÃO DE AFILIADO
AFFILIATE_ID = "seu-id-afiliado"
AFFILIATE_BASE_URL = "https://seusite.com/afiliado/"

# ==============================================================================
# FILTROS DE PRODUTOS PERMITIDOS
# ==============================================================================
ALLOWED_KEYWORDS = [
    # Componentes Essenciais
    'processador', 'cpu', 'intel', 'amd', 'ryzen', 'core i3', 'core i5', 'core i7', 'core i9',
    'memória ram', 'memoria ram', 'ddr4', 'ddr5', 'ram',
    'ssd', 'nvme', 'm.2', 'sata', 'armazenamento', 'hd', 'disco',
    'placa mãe', 'placa-mãe', 'motherboard', 'placa mae',
    'placa de vídeo', 'placa de video', 'gpu', 'geforce', 'rtx', 'gtx', 'radeon', 'rx',
    'fonte', 'psu', 'alimentação', 'alimentacao',
    'gabinete', 'case', 'tower',
    
    # Periféricos
    'monitor', 'display', 'tela',
    'teclado', 'keyboard', 'mecânico', 'mecanico',
    'mouse', 'gamer',
    'webcam', 'camera web',
    'microfone', 'mic',
    'headset', 'fone', 'headphone', 'caixa de som', 'speaker',
    
    # Conforto e Ergonomia
    'cadeira gamer', 'cadeira ergonomica', 'cadeira escritorio',
    'mesa gamer', 'mesa escritorio', 'escrivaninha',
    'mousepad', 'apoio pulso', 'descanso pulso',
    'luminária', 'luminaria', 'led', 'iluminação',
    'suporte monitor', 'braço monitor',
    
    # Outros relacionados a PC
    'notebook', 'laptop',
    'cooler', 'ventilador', 'water cooler', 'refrigeração',
    'pasta térmica', 'pasta termica',
    'cabo hdmi', 'cabo displayport', 'cabo usb',
    'hub usb', 'adaptador',
    'no-break', 'nobreak', 'estabilizador',
    
    # Celulares e Tablets
    'celular', 'smartphone', 'iphone', 'galaxy', 'xiaomi', 'motorola', 'samsung',
    'redmi', 'poco', 'realme', 'asus phone', 'lg phone',
    'tablet', 'ipad', 'galaxy tab',
    
    # TVs
    'tv', 'televisão', 'televisao', 'smart tv', 'tv led', 'tv oled', 'tv qled',
    'tv 4k', 'tv 8k', 'android tv', 'google tv', 'fire tv',
    
    # Consoles e Gaming
    'console', 'playstation', 'ps5', 'ps4', 'ps3', 'psvr',
    'xbox', 'xbox series x', 'xbox series s', 'xbox one',
    'nintendo', 'switch', 'nintendo switch', 'switch oled',
    'steam deck', 'controle', 'joystick', 'gamepad',
    'jogo', 'game', 'ps plus', 'xbox game pass'
]

BLOCKED_KEYWORDS = [
    # Produtos realmente não relacionados (mantém bloqueio de coisas inúteis)
    'roupa', 'camisa', 'camiseta', 'calça', 'sapato', 'tênis', 'bermuda', 'blusa',
    'livro', 'revista', 'gibi',
    'brinquedo', 'boneca', 'carrinho de brinquedo',
    'perfume', 'cosmético', 'maquiagem', 'shampoo',
    'alimento', 'comida', 'bebida', 'chocolate',
    'eletrodoméstico', 'geladeira', 'fogão', 'microondas', 'liquidificador',
    'carro', 'moto', 'peça automotiva', 'pneu',
    'imóvel', 'apartamento', 'casa',
    'relógio de pulso', 'joia', 'anel', 'colar',
    'instrumento musical', 'violão', 'guitarra', 'bateria',
    'esporte', 'bola de futebol', 'bicicleta', 'esteira',
    'pet', 'cachorro', 'gato', 'ração', 'coleira'
]

def is_pc_related_product(title):
    """
    Verifica se o produto é relacionado a tecnologia/gaming usando palavras-chave.
    
    Args:
        title (str): Título do produto
        
    Returns:
        bool: True se for relacionado a tech/gaming, False caso contrário
    """
    title_lower = title.lower()
    
    # Verifica se contém palavras bloqueadas
    for blocked in BLOCKED_KEYWORDS:
        if blocked in title_lower:
            print(f"  ❌ Bloqueado por: '{blocked}'")
            return False
    
    # Verifica se contém palavras permitidas
    for keyword in ALLOWED_KEYWORDS:
        if keyword in title_lower:
            print(f"  ✅ Permitido por: '{keyword}'")
            return True
    
    # Se não encontrou nenhuma palavra-chave permitida, bloqueia
    print(f"  ⚠️ Não encontrou palavras-chave relacionadas a tech/gaming")
    return False

# ==============================================================================
# CONFIGURAÇÃO DO BANCO DE DADOS MYSQL
# ==============================================================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sua senha aqui',
    'database': 'bot_ofertas'
}

# ==============================================================================
# CONFIGURAÇÃO DE SITES PARA SCRAPING
# ==============================================================================
SCRAPING_TARGETS = [
    {
        "name": "Mercado Livre - Informática",
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
        "name": "Mercado Livre - Celulares e Telefones",
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
        "name": "Mercado Livre - Consoles e Video Games",
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
]

# ==============================================================================
# FUNÇÕES DO BANCO DE DADOS
# ==============================================================================
def create_database_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        return None

def initialize_database():
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"✅ Banco de dados '{DB_CONFIG['database']}' verificado/criado")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Tabela de ofertas enviadas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ofertas_enviadas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hash_oferta VARCHAR(64) UNIQUE NOT NULL,
                titulo VARCHAR(500) NOT NULL,
                preco VARCHAR(50),
                link TEXT NOT NULL,
                fonte VARCHAR(100),
                data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_hash (hash_oferta),
                INDEX idx_data (data_envio)
            )
        """)
        
        # Tabela de fila de ofertas (para envio programado)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fila_ofertas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hash_oferta VARCHAR(64) UNIQUE NOT NULL,
                dados_oferta TEXT NOT NULL,
                fonte VARCHAR(100),
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_fonte (fonte),
                INDEX idx_data (data_criacao)
            )
        """)
        
        print("✅ Tabelas verificadas/criadas")
        cursor.close()
        connection.close()
    except Error as e:
        print(f"❌ Erro ao inicializar banco: {e}")

def generate_offer_hash(title, link):
    clean_link = link.split('?')[0].split('#')[0]
    offer_string = f"{title.lower().strip()}|{clean_link}"
    return hashlib.sha256(offer_string.encode()).hexdigest()

def is_offer_already_sent(offer_hash):
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
    connection = create_database_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        offer_hash = generate_offer_hash(offer['title'], offer['link'])
        cursor.execute("""
            INSERT INTO ofertas_enviadas (hash_oferta, titulo, preco, link, fonte)
            VALUES (%s, %s, %s, %s, %s)
        """, (offer_hash, offer['title'][:500], offer['price'], offer['link'], offer['source']))
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
        cursor.execute("""
            INSERT IGNORE INTO fila_ofertas (hash_oferta, dados_oferta, fonte)
            VALUES (%s, %s, %s)
        """, (offer_hash, dados_json, offer['source']))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"❌ Erro ao adicionar à fila: {e}")
        return False

def get_next_offer_from_queue(source):
    """Pega a próxima oferta da fila de uma fonte específica"""
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
            # Remove da fila
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
    """Retorna quantidade de ofertas na fila por fonte"""
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
    connection = create_database_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as total FROM ofertas_enviadas")
        total = cursor.fetchone()['total']
        cursor.execute("""
            SELECT COUNT(*) as hoje 
            FROM ofertas_enviadas 
            WHERE DATE(data_envio) = CURDATE()
        """)
        hoje = cursor.fetchone()['hoje']
        cursor.execute("""
            SELECT fonte, COUNT(*) as quantidade 
            FROM ofertas_enviadas 
            GROUP BY fonte 
            ORDER BY quantidade DESC
        """)
        por_fonte = cursor.fetchall()
        cursor.close()
        connection.close()
        return {'total': total, 'hoje': hoje, 'por_fonte': por_fonte}
    except Error as e:
        print(f"❌ Erro ao buscar estatísticas: {e}")
        return None

# ==============================================================================
# WEB SCRAPING COM SELENIUM
# ==============================================================================
async def scrape_offers_with_selenium(target_site, max_pages=5):
    """Faz scraping usando Selenium com WebDriver Manager - múltiplas páginas se necessário"""
    print(f"🔍 Iniciando scraping em: {target_site['name']}")
    all_offers = []
    
    for page_num in range(1, max_pages + 1):
        # Modifica URL para incluir número da página
        url = target_site['url']
        if 'page=' in url:
            url = re.sub(r'page=\d+', f'page={page_num}', url)
        elif '?' in url:
            url = f"{url}&page={page_num}"
        else:
            url = f"{url}?page={page_num}"
        
        print(f"📄 Página {page_num}/{max_pages}: {url}")
        
        offers = await asyncio.to_thread(scrape_offers_sync, target_site, url)
        
        if not offers:
            print(f"⚠️ Nenhuma oferta encontrada na página {page_num}, parando busca neste site.")
            break
        
        all_offers.extend(offers)
        print(f"✅ {len(offers)} ofertas extraídas da página {page_num}")
        
        # Se já pegou ofertas suficientes, para
        if len(all_offers) >= 50:
            print(f"✅ Limite de 50 ofertas atingido, parando busca.")
            break
        
        # Pequena pausa entre páginas
        await asyncio.sleep(2)
    
    return all_offers

def scrape_offers_sync(target_site, url):
    """Função síncrona de scraping para Selenium"""
    offers = []
    driver = None
    
    try:
        # Configura opções do Chrome - SEM HEADLESS para melhor captura
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # DESABILITADO para melhor performance
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--start-maximized')  # Maximizado para carregar todas imagens
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Habilita imagens
        prefs = {"profile.managed_default_content_settings.images": 1}
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Inicia o driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print(f"📡 Acessando: {url}")
        driver.get(url)
        
        # Aguarda carregamento MAIOR para garantir imagens
        time.sleep(6)
        
        # Scroll múltiplo para carregar TODAS as imagens
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*3/4);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        # Volta pro topo para processar
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        # Obtém HTML
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        
        # Busca produtos
        products = soup.select(target_site['selectors']['container'])
        print(f"✅ Encontrados {len(products)} produtos")
        
        # Se não encontrou, tenta seletores alternativos
        if len(products) == 0:
            print("🔄 Tentando seletores alternativos...")
            alternative_selectors = [
                'li.ui-search-layout__item',
                'div.ui-search-result',
                'div.poly-card',
                'article.ui-search-result',
                'div[class*="item"]',
                'li[class*="item"]'
            ]
            for alt_selector in alternative_selectors:
                products = soup.select(alt_selector)
                if len(products) > 0:
                    print(f"✅ Encontrados {len(products)} com {alt_selector}")
                    target_site['selectors']['container'] = alt_selector
                    break
        
        # Processa TODOS os produtos da página
        for idx, product in enumerate(products):
            try:
                title_elem = (product.select_one(target_site['selectors']['title']) or 
                             product.select_one('h2') or 
                             product.select_one('h3') or
                             product.select_one('[class*="title"]') or
                             product.select_one('[class*="name"]'))
                
                price_elem = (product.select_one(target_site['selectors']['price']) or
                             product.select_one('[class*="price-tag-fraction"]') or
                             product.select_one('[class*="price"]') or
                             product.select_one('span[class*="andes-money-amount"]'))
                
                link_elem = (product.select_one(target_site['selectors']['link']) or
                            product.select_one('a[href*="produto"]') or
                            product.select_one('a[href*="MLB"]') or
                            product.select_one('a'))
                
                if not (title_elem and price_elem and link_elem):
                    continue
                
                original_link = link_elem.get('href', '')
                if not original_link:
                    original_link = product.get('href', '')
                
                if not original_link.startswith('http'):
                    from urllib.parse import urljoin
                    original_link = urljoin(url, original_link)
                
                if 'mercadolivre' in original_link or 'mercadolibre' in original_link:
                    original_link = original_link.split('#')[0].split('?')[0]
                
                title = title_elem.get_text(strip=True)
                if len(title) < 10:
                    continue
                
                # FILTRO: Verifica se é relacionado a PC
                print(f"\n🔍 Analisando: {title[:60]}...")
                if not is_pc_related_product(title):
                    print(f"  🚫 Produto ignorado (não relacionado a PC)")
                    continue
                
                print(f"  ✅ Produto aceito!")
                
                # BUSCA AGRESSIVA DE IMAGEM - múltiplos métodos
                image_url = None
                
                # Método 1: Seletor específico
                if 'image' in target_site['selectors']:
                    image_elem = product.select_one(target_site['selectors']['image'])
                    if image_elem:
                        image_url = (image_elem.get('data-src') or 
                                   image_elem.get('src') or 
                                   image_elem.get('data-lazy-src') or
                                   image_elem.get('data-original') or
                                   image_elem.get('data-zoom'))
                
                # Método 2: Busca todas as imgs
                if not image_url:
                    all_imgs = product.select('img')
                    for img in all_imgs:
                        potential_url = (img.get('data-src') or 
                                       img.get('src') or 
                                       img.get('data-lazy-src') or
                                       img.get('data-original') or
                                       img.get('srcset', '').split(',')[0].split(' ')[0])
                        
                        # Valida URL de imagem
                        if potential_url and 'http' in potential_url:
                            # Ignora placeholders
                            if not any(x in potential_url.lower() for x in ['blank', 'placeholder', 'loading', 'sprite', '1x1']):
                                image_url = potential_url
                                break
                
                # Método 3: Busca por picture > img
                if not image_url:
                    picture = product.select_one('picture')
                    if picture:
                        img = picture.select_one('img')
                        if img:
                            image_url = (img.get('data-src') or img.get('src'))
                
                # Limpa URL da imagem (remove parâmetros de tamanho pequeno)
                if image_url:
                    # Mercado Livre usa parâmetros como -I.jpg, troca por tamanho maior
                    if 'mlstatic.com' in image_url or 'mlu.com' in image_url:
                        image_url = re.sub(r'-[IOP]\.jpg', '-W.jpg', image_url)  # W = maior tamanho
                        image_url = image_url.split('?')[0]  # Remove query params
                
                if image_url:
                    print(f"  🖼️ Imagem: {image_url[:70]}...")
                else:
                    print(f"  ⚠️ SEM imagem: {title[:50]}...")
                
                offer = {
                    "title": title[:200],
                    "price": clean_price(price_elem.get_text(strip=True)),
                    "original_price": None,
                    "link": create_affiliate_link(original_link),
                    "source": target_site['name'],
                    "image_url": image_url
                }
                
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
    
    print(f"📊 Total extraídas desta página: {len(offers)}")
    return offers

# ==============================================================================
# FUNÇÕES AUXILIARES
# ==============================================================================
def create_affiliate_link(original_link):
    return original_link

def clean_price(price_text):
    price = re.sub(r'[^\d,.]', '', price_text)
    if '.' in price and ',' in price:
        price = price.replace('.', '').replace(',', '.')
    return f"R$ {price}" if price else "Consultar"

def calculate_discount(original_price, current_price):
    try:
        original = float(re.sub(r'[^\d.]', '', original_price))
        current = float(re.sub(r'[^\d.]', '', current_price))
        if original > current:
            discount_percent = ((original - current) / original) * 100
            return f"{int(discount_percent)}% OFF"
    except:
        pass
    return None

# ==============================================================================
# LÓGICA PRINCIPAL - BUSCA E FILA
# ==============================================================================
async def find_and_manage_offers(context: ContextTypes.DEFAULT_TYPE):
    """Busca ofertas continuamente até encontrar novas"""
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
        max_attempts = 10  # Tenta até 10 vezes (até 10 páginas)
        
        # Continua buscando até encontrar ofertas novas OU atingir limite
        while not found_new and attempts < max_attempts:
            attempts += 1
            print(f"\n🔄 Tentativa {attempts}/{max_attempts} para {target['name']}")
            
            # Busca com paginação (busca até 5 páginas por tentativa)
            offers = await scrape_offers_with_selenium(target, max_pages=5)
            
            if not offers:
                print(f"⚠️ Nenhuma oferta encontrada, tentando novamente...")
                await asyncio.sleep(3)
                continue
            
            # Filtra ofertas não enviadas
            new_offers = []
            for offer in offers:
                offer_hash = generate_offer_hash(offer['title'], offer['link'])
                if not is_offer_already_sent(offer_hash):
                    new_offers.append(offer)
            
            print(f"\n📊 Resultado da tentativa {attempts}:")
            print(f"  • Total encontradas: {len(offers)}")
            print(f"  • Já enviadas (duplicadas): {len(offers) - len(new_offers)}")
            print(f"  • Novas (não enviadas): {len(new_offers)}")
            
            if new_offers:
                found_new = True
                print(f"\n✅ Encontradas {len(new_offers)} ofertas NOVAS de {target['name']}!")
                
                # Envia APENAS a primeira
                first_offer = new_offers[0]
                print(f"\n📤 Enviando primeira oferta: {first_offer['title'][:50]}...")
                success = await send_offer_to_group(context, first_offer)
                
                if success:
                    save_sent_offer(first_offer)
                    total_new_offers += 1
                    print(f"✅ Oferta enviada e salva no banco!")
                
                # Adiciona o restante à fila
                if len(new_offers) > 1:
                    print(f"\n📥 Adicionando {len(new_offers) - 1} ofertas à fila:")
                    for offer in new_offers[1:]:
                        add_to_queue(offer)
                        print(f"  ✓ {offer['title'][:50]}...")
            else:
                print(f"⚠️ Todas as {len(offers)} ofertas já foram enviadas anteriormente.")
                print(f"🔄 Buscando em páginas seguintes...")
                await asyncio.sleep(2)
        
        if not found_new:
            print(f"\n❌ Não foram encontradas ofertas novas de {target['name']} após {max_attempts} tentativas.")
            print(f"💡 Todas as ofertas disponíveis já foram enviadas!")
        
        # Pequena pausa entre fontes
        await asyncio.sleep(3)
    
    # Resumo final
    queue_counts = get_queue_count()
    print(f"\n" + "="*60)
    print(f"📊 RESUMO DA BUSCA")
    print(f"="*60)
    print(f"✅ Ofertas enviadas agora: {total_new_offers}")
    print(f"📥 Total na fila: {sum(queue_counts.values())}")
    for fonte, qtd in queue_counts.items():
        print(f"  • {fonte}: {qtd}")
    print(f"="*60)

async def send_queued_offers(context: ContextTypes.DEFAULT_TYPE):
    """Envia 1 oferta da fila de cada categoria"""
    print("\n⏰ Enviando ofertas da fila...")
    
    for target in SCRAPING_TARGETS:
        offer = get_next_offer_from_queue(target['name'])
        if offer:
            success = await send_offer_to_group(context, offer)
            if success:
                save_sent_offer(offer)
                print(f"✅ Enviada da fila: {offer['title'][:40]}...")
            await asyncio.sleep(2)

async def check_and_search_if_needed(context: ContextTypes.DEFAULT_TYPE):
    """Verifica fila e busca novas ofertas se estiver vazia"""
    queue_counts = get_queue_count()
    total_in_queue = sum(queue_counts.values())
    
    print(f"\n🔍 Verificando fila: {total_in_queue} ofertas")
    
    if total_in_queue < 5:  # Se tiver menos de 5 na fila
        print("⚠️ Fila baixa! Buscando novas ofertas...")
        await find_and_manage_offers(context)

# ==============================================================================
# ENVIO DE OFERTAS
# ==============================================================================
async def send_offer_to_group(context: ContextTypes.DEFAULT_TYPE, offer):
    caption = f"🔥 *OFERTA ENCONTRADA* 🔥\n"
    caption += "━━━━━━━━━━━━━━━━━━━━\n\n"
    caption += f"📦 *{offer['title']}*\n\n"
    
    if offer.get('original_price') and offer.get('discount'):
        caption += f"💰 ~~{offer['original_price']}~~ ➜ *{offer['price']}*\n"
        caption += f"🏷️ *{offer['discount']}*\n\n"
    else:
        caption += f"💰 *{offer['price']}*\n\n"
    
    caption += f"🛒 [👉 COMPRAR AGORA]({offer['link']})\n\n"
    caption += f"📍 {offer['source']}\n"
    caption += f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    
    try:
        if offer.get('image_url'):
            await context.bot.send_photo(
                chat_id=GROUP_CHAT_ID,
                photo=offer['image_url'],
                caption=caption,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await context.bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=caption,
                parse_mode=ParseMode.MARKDOWN
            )
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar: {e}")
        return False

# ==============================================================================
# COMANDOS
# ==============================================================================
async def buscar_ofertas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Buscando ofertas...")
    await find_and_manage_offers(context)
    await update.message.reply_text("✅ Busca concluída!")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = get_statistics()
    queue_counts = get_queue_count()
    
    msg = f"🤖 *Status do Bot*\n\n"
    msg += f"✅ Bot ativo\n"
    msg += f"🔍 Sites: {len(SCRAPING_TARGETS)}\n\n"
    
    if stats:
        msg += f"📊 *Estatísticas:*\n"
        msg += f"📦 Total enviadas: {stats['total']}\n"
        msg += f"📅 Hoje: {stats['hoje']}\n\n"
    
    msg += f"📥 *Fila de ofertas:*\n"
    total_fila = sum(queue_counts.values())
    msg += f"Total na fila: {total_fila}\n"
    for fonte, qtd in queue_counts.items():
        msg += f"  • {fonte}: {qtd}\n"
    
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    print("="*60)
    print("🤖 BOT DE OFERTAS COM FILA INTELIGENTE")
    print("="*60)
    
    initialize_database()
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("buscar", buscar_ofertas_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # AGENDAMENTO:
    # 1. Envia ofertas da fila a cada 10 minutos
    application.job_queue.run_repeating(send_queued_offers, interval=600, first=30)
    
    # 2. Verifica e busca novas se necessário a cada 30 minutos
    application.job_queue.run_repeating(check_and_search_if_needed, interval=1800, first=60)
    
    print("✅ Bot iniciado com sistema de fila!")
    print("⏰ Envio da fila: a cada 10 minutos")
    print("🔄 Verificação: a cada 30 minutos\n")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()