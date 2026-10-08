import asyncio

from ofertas import jobs

TARGETS = [{"name": "A"}, {"name": "B"}, {"name": "C"}]


def _setup(monkeypatch, queues, clock):
    sent = []

    async def fake_send(context, offer):
        sent.append(offer["title"])
        return True

    def fake_next(source):
        queue = queues.get(source, [])
        return queue.pop(0) if queue else None

    monkeypatch.setattr(jobs, "SCRAPING_TARGETS", TARGETS)
    monkeypatch.setattr(jobs, "send_offer_to_group", fake_send)
    monkeypatch.setattr(jobs, "get_next_offer_from_queue", fake_next)
    monkeypatch.setattr(jobs, "save_sent_offer", lambda offer: True)
    monkeypatch.setattr(jobs, "get_send_interval", lambda: 600)
    monkeypatch.setattr(jobs, "_now", lambda: clock[0])
    monkeypatch.setattr(jobs, "_last_send_at", None)
    monkeypatch.setattr(jobs, "_next_source", 0)
    return sent


def _offer(title):
    return {"title": title, "image_url": "https://x/y.jpg"}


def test_envia_uma_por_vez_e_respeita_o_intervalo(monkeypatch):
    clock = [1000.0]
    queues = {"A": [_offer("a1"), _offer("a2")], "B": [_offer("b1")], "C": []}
    sent = _setup(monkeypatch, queues, clock)

    asyncio.run(jobs.send_queued_offers(None))
    assert sent == ["a1"]          # só uma, não uma por fonte

    clock[0] += 60                 # passou 1 min: ainda não é hora
    asyncio.run(jobs.send_queued_offers(None))
    assert sent == ["a1"]

    clock[0] += 600                # passou o intervalo: próxima fonte
    asyncio.run(jobs.send_queued_offers(None))
    assert sent == ["a1", "b1"]

    clock[0] += 600                # C vazia, volta para A
    asyncio.run(jobs.send_queued_offers(None))
    assert sent == ["a1", "b1", "a2"]


def test_fila_vazia_nao_envia_nem_trava(monkeypatch):
    clock = [1000.0]
    sent = _setup(monkeypatch, {}, clock)
    asyncio.run(jobs.send_queued_offers(None))
    assert sent == []
    assert jobs._last_send_at is None
