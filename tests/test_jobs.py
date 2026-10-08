import asyncio

from ofertas import jobs


def _offer(n):
    return {"title": f"Produto de teste {n}", "link": f"https://produto.mercadolivre.com.br/MLB-{n}"}


def _fake_pages(pages, visited):
    async def iter_listing_pages(target, max_pages):
        for number, page in enumerate(pages[:max_pages], start=1):
            visited.append(number)
            yield page
    return iter_listing_pages


def test_pula_enviadas_e_repetidas_entre_paginas(monkeypatch):
    visited = []
    pages = [[_offer(1), _offer(2)], [_offer(2), _offer(3)]]
    already_sent = {jobs.generate_offer_hash(_offer(1)["title"], _offer(1)["link"])}
    monkeypatch.setattr(jobs, "iter_listing_pages", _fake_pages(pages, visited))
    monkeypatch.setattr(jobs, "is_offer_already_sent", lambda h: h in already_sent)

    new_offers = asyncio.run(jobs.collect_new_offers({"name": "teste"}))

    assert [o["title"] for o in new_offers] == ["Produto de teste 2", "Produto de teste 3"]
    assert visited == [1, 2]


def test_para_de_paginar_quando_ja_tem_novas_suficientes(monkeypatch):
    visited = []
    pages = [[_offer(n) for n in range(10)], [_offer(n) for n in range(10, 20)], [_offer(99)]]
    monkeypatch.setattr(jobs, "iter_listing_pages", _fake_pages(pages, visited))
    monkeypatch.setattr(jobs, "is_offer_already_sent", lambda h: False)
    monkeypatch.setattr(jobs, "NEW_OFFERS_WANTED", 15)

    new_offers = asyncio.run(jobs.collect_new_offers({"name": "teste"}))

    assert len(new_offers) == 20
    assert visited == [1, 2]
