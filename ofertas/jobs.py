"""Rotinas agendadas: buscar ofertas, abastecer a fila e enviar."""

import asyncio
from contextlib import aclosing
from datetime import datetime

from telegram.ext import ContextTypes

from .config import SCRAPING_TARGETS
from .database import (
    add_to_queue,
    generate_offer_hash,
    get_next_offer_from_queue,
    get_queue_count,
    is_offer_already_sent,
    save_sent_offer,
)
from .scheduling import get_offers_per_hour
from .scraper import iter_listing_pages
from .sender import send_offer_to_group

# ═════════════════════════════════════════════════════════════════════════════
# LÓGICA PRINCIPAL
# ═════════════════════════════════════════════════════════════════════════════

# Quantas páginas de cada fonte olhar por busca e quantas ofertas novas
# bastam para parar de paginar
MAX_PAGES = 5
NEW_OFFERS_WANTED = 20

async def collect_new_offers(target):
    """Percorre as páginas da fonte e junta as ofertas que ainda não foram enviadas"""
    new_offers = []
    seen_hashes = set()

    async with aclosing(iter_listing_pages(target, max_pages=MAX_PAGES)) as pages:
        async for offers in pages:
            new_in_page = 0
            for offer in offers:
                offer_hash = generate_offer_hash(offer['title'], offer['link'])
                if offer_hash in seen_hashes or is_offer_already_sent(offer_hash):
                    continue
                seen_hashes.add(offer_hash)
                new_offers.append(offer)
                new_in_page += 1

            print(f"  📊 Página: {len(offers)} ofertas, {new_in_page} novas")

            if len(new_offers) >= NEW_OFFERS_WANTED:
                break

    return new_offers

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

        new_offers = await collect_new_offers(target)

        if not new_offers:
            print(f"\n❌ Nenhuma oferta nova nas primeiras {MAX_PAGES} páginas")
            await asyncio.sleep(3)
            continue

        print(f"\n✅ Encontradas {len(new_offers)} ofertas NOVAS!")

        # FILTRO: Remove ofertas sem imagem (a oferta é enviada como foto)
        valid_offers = []
        for offer in new_offers:
            if offer.get('image_url'):
                valid_offers.append(offer)
            else:
                print(f"  🚫 Ignorando: {offer['title'][:50]} (sem imagem)")

        if not valid_offers:
            print(f"  ⚠️ Nenhuma oferta válida (todas sem imagem)")
            await asyncio.sleep(3)
            continue

        print(f"\n✅ {len(valid_offers)} ofertas válidas (com imagem)")

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
            if not offer.get('image_url'):
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
