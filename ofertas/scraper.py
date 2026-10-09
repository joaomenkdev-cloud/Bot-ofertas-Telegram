"""Scraping das páginas de listagem com Selenium."""

import asyncio
import re
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .affiliates import create_affiliate_link
from .config import CHROME_PROFILE_DIR
from .filters import is_pc_related_product
from .prices import calculate_discount, clean_price

# ID da imagem nas URLs do mlstatic, ex.: 900577-MLB97918475120_112025
ML_IMAGE_ID = re.compile(r"(\d+-[A-Z]+\d+_\d+)-")

# ═════════════════════════════════════════════════════════════════════════════
# WEB SCRAPING COM SELENIUM
# ═════════════════════════════════════════════════════════════════════════════

async def iter_listing_pages(target_site, max_pages=5):
    """
    Percorre a listagem página por página, devolvendo as ofertas de cada uma.
    Segue o botão "Seguinte" da própria página: o ML pagina com _Desde_N nas
    listagens e com ?page=N em outras, então montar a URL na mão não funciona.
    Usa um único Chrome para todas as páginas da busca.
    """
    print(f"🔍 Iniciando scraping em: {target_site['name']}")
    url = target_site['url']
    driver = None
    
    try:
        driver = await asyncio.to_thread(create_driver)
        
        for page_num in range(1, max_pages + 1):
            print(f"📄 Página {page_num}/{max_pages}")
            
            offers, next_url = await asyncio.to_thread(scrape_offers_sync, driver, target_site, url)
            
            if offers:
                print(f"✅ {len(offers)} ofertas extraídas")
                yield offers
            else:
                print(f"⚠️ Nenhuma oferta nesta página")
            
            if not next_url:
                print(f"ℹ️ Não há próxima página")
                break
            
            url = next_url
            await asyncio.sleep(1)
    except WebDriverException as e:
        print(f"❌ Erro no Chrome: {e.msg}")
    finally:
        if driver:
            await asyncio.to_thread(driver.quit)

def scrape_offers_sync(driver, target_site, url):
    """Função síncrona de scraping: devolve (ofertas, URL da próxima página)"""
    try:
        page_source = fetch_page_html(driver, url, target_site['selectors']['container'])
    except BotBlockedError:
        return [], None
    except WebDriverException as e:
        print(f"❌ Erro ao abrir a página: {e.msg}")
        return [], None
    
    offers = parse_listing(page_source, target_site, url)
    print(f"📊 Total extraídas: {len(offers)}")
    return offers, find_next_page_url(page_source, url)

def find_next_page_url(page_source, url):
    """Lê o link do botão "Seguinte" da paginação (None na última página)"""
    soup = BeautifulSoup(page_source, 'lxml')
    next_link = soup.select_one(
        'li.andes-pagination__button--next:not(.andes-pagination__button--disabled) a[href]'
    )
    if next_link is None:
        return None
    return urljoin(url, next_link['href'])

class BotBlockedError(WebDriverException):
    """O site pediu verificação/login e não entregou a página"""

def create_driver():
    """Abre o Chrome (o Selenium baixa o chromedriver certo sozinho)"""
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    # Perfil próprio do bot: guarda o login do Mercado Livre entre as execuções
    chrome_options.add_argument(f'--user-data-dir={CHROME_PROFILE_DIR}')
    
    # Habilita imagens
    prefs = {"profile.managed_default_content_settings.images": 1}
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(60)
    return driver

def fetch_page_html(driver, url, container_selector):
    """Abre a página e devolve o HTML renderizado, com as imagens já carregadas"""
    print(f"📡 Acessando: {url}")
    driver.get(url)
    
    # O ML às vezes pede login antes de mostrar a listagem (verificação anti-robô)
    if 'account-verification' in driver.current_url:
        print("🔒 O Mercado Livre pediu login/verificação de conta e não mostrou a listagem.")
        print("   Rode `python bot.py --login` e entre na sua conta nessa janela (uma vez só).")
        raise BotBlockedError("verificação de conta do Mercado Livre")
    
    # Espera os cards aparecerem em vez de dormir um tempo fixo
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, container_selector))
        )
    except TimeoutException:
        print("⚠️ Os cards não apareceram a tempo")
        return driver.page_source
    
    # Rola a página aos poucos para o lazy-load das imagens
    for fraction in ("1/4", "1/2", "3/4", "1"):
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight*{fraction});")
        time.sleep(1)
    
    return driver.page_source

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

def login_interactive():
    """Abre o Chrome do bot para você entrar na sua conta do Mercado Livre"""
    driver = create_driver()
    try:
        driver.get("https://www.mercadolivre.com.br/")
        print()
        print("👉 Entre na sua conta do Mercado Livre na janela que abriu.")
        input("Quando terminar o login, volte aqui e aperte Enter... ")
    finally:
        driver.quit()
    print(f"✅ Sessão salva em {CHROME_PROFILE_DIR}")
