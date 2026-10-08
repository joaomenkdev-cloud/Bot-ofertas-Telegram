"""Scraping das páginas de listagem com Selenium."""

import asyncio
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from .affiliates import create_affiliate_link
from .filters import is_pc_related_product
from .prices import calculate_discount, clean_price

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
            
        except Exception:
            continue
    
    return offers
