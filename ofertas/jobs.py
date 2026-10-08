"""Rotinas agendadas: buscar ofertas, abastecer a fila e enviar."""

import asyncio
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
from .scraper import scrape_offers_with_selenium
from .sender import send_offer_to_group

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
