"""Scraping das páginas de listagem com Selenium."""

import asyncio
import re
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from .affiliates import create_affiliate_link
from .filters import is_pc_related_product
from .prices import calculate_discount, clean_price

# ID da imagem nas URLs do mlstatic, ex.: 900577-MLB97918475120_112025
ML_IMAGE_ID = re.compile(r"(\d+-[A-Z]+\d+_\d+)-")

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
    try:
        page_source = fetch_page_html(url)
    except Exception as e:
        print(f"❌ Erro no scraping: {e}")
        import traceback
        traceback.print_exc()
        return []
    
    offers = parse_listing(page_source, target_site, url)
    print(f"📊 Total extraídas: {len(offers)}")
    return offers

def fetch_page_html(url):
    """Abre a página no Chrome e devolve o HTML renderizado"""
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
        
        return driver.page_source
    finally:
        if driver:
            driver.quit()

def parse_listing(page_source, target_site, url):
    """Extrai as ofertas do HTML de uma página de listagem"""
    offers = []
    soup = BeautifulSoup(page_source, 'lxml')
    selectors = target_site['selectors']

    # Busca produtos
    products = soup.select(selectors['container'])
    print(f"✅ Encontrados {len(products)} produtos")

    # Seletores alternativos se não encontrar
    if len(products) == 0:
        print("🔄 Tentando seletores alternativos...")
        alternative_selectors = [
            'li.ui-search-layout__item',
            'div.ui-search-result',
        ]
        for alt_selector in alternative_selectors:
            products = soup.select(alt_selector)
            if len(products) > 0:
                print(f"✅ Encontrados {len(products)} com {alt_selector}")
                break

    # Processa cada produto
    for product in products:
        try:
            offer = extract_offer(product, target_site, url)
        except Exception as e:
            print(f"  ⚠️ Erro ao ler um card de produto: {e}")
            continue
        if offer:
            offers.append(offer)

    return offers

def extract_offer(product, target_site, url):
    """Monta a oferta a partir de um card de produto (ou None se não servir)"""
    selectors = target_site['selectors']

    # Extrai título
    title_elem = (product.select_one(selectors['title']) or
                  product.select_one('h2') or
                  product.select_one('h3'))

    # Extrai link
    link_elem = (product.select_one(selectors['link']) or
                 product.select_one('a[href]'))

    # Extrai preço atual (o primeiro preço do card é o antigo, riscado)
    price_text = read_money(product.select_one(selectors['price']))

    if not (title_elem and link_elem and price_text):
        return None

    title = title_elem.get_text(strip=True)
    if len(title) < 10:
        return None

    original_link = urljoin(url, link_elem.get('href', ''))

    # Anúncios patrocinados apontam para um link de rastreio (click1...)
    # que não tem o ID do produto; cortar a query quebraria o link
    if 'click1.mercadolivre' in original_link:
        print(f"  ⏭️ Anúncio patrocinado ignorado: {title[:50]}")
        return None

    # Limpa a URL
    if 'mercadolivre' in original_link:
        original_link = original_link.split('#')[0].split('?')[0]

    # FILTRO: Verifica se é produto aceito
    print(f"\n🔍 Analisando: {title[:60]}...")
    if not is_pc_related_product(title):
        print(f"  🚫 Produto ignorado")
        return None

    print(f"  ✅ Produto aceito!")

    image_url = find_image_url(product, selectors)
    if image_url:
        print(f"  🖼️ Imagem encontrada")
    else:
        print(f"  ⚠️ Sem imagem")

    # Cria link de afiliado (se configurado)
    affiliate_link = create_affiliate_link(original_link, target_site.get('platform'))
    has_affiliate = (affiliate_link != original_link)

    # Cria objeto da oferta
    offer = {
        "title": title[:200],
        "price": clean_price(price_text),
        "original_price": None,
        "link": affiliate_link,
        "original_link": original_link,
        "source": target_site['name'],
        "platform": target_site.get('platform', 'desconhecido'),
        "image_url": image_url,
        "has_affiliate": has_affiliate
    }

    # Busca preço original (se tiver)
    original_price_text = read_money(product.select_one(selectors['original_price']))
    if original_price_text:
        offer['original_price'] = clean_price(original_price_text)
        offer['discount'] = calculate_discount(offer['original_price'], offer['price'])
        if not offer['discount']:
            offer['original_price'] = None

    return offer

def read_money(amount_elem):
    """
    Lê um bloco .andes-money-amount do ML: reais e centavos ficam em spans
    separados (__fraction e __cents). Devolve texto como "1.299,90".
    """
    if amount_elem is None:
        return None
    fraction = amount_elem.select_one('.andes-money-amount__fraction')
    if fraction is None:
        return None
    text = fraction.get_text(strip=True)
    cents = amount_elem.select_one('.andes-money-amount__cents')
    if cents is not None:
        text += f",{cents.get_text(strip=True)}"
    return text

def find_image_url(product, selectors):
    """Acha a imagem do produto e troca pela versão grande em JPEG"""
    candidates = []
    image_elem = product.select_one(selectors.get('image', '')) if selectors.get('image') else None
    if image_elem:
        candidates.append(image_elem)
    candidates.extend(product.select('img'))

    for img in candidates:
        potential_url = img.get('data-src') or img.get('src')
        if potential_url and potential_url.startswith('http'):
            if not any(x in potential_url.lower() for x in ['blank', 'placeholder']):
                return full_size_ml_image(potential_url)
    return None

def full_size_ml_image(image_url):
    """
    As listagens do ML trazem miniaturas em WebP
    (D_Q_NP_2X_900577-MLB979..._112025-AB-nome.webp). O mesmo ID serve a
    versão grande em JPEG (D_NQ_NP_900577-MLB979..._112025-O.jpg), formato
    que o Telegram aceita sem problema por URL.
    """
    if 'mlstatic.com' not in image_url:
        return image_url
    match = ML_IMAGE_ID.search(image_url)
    if not match:
        return image_url.split('?')[0]
    return f"https://http2.mlstatic.com/D_NQ_NP_{match.group(1)}-O.jpg"
