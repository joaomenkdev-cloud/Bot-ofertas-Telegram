from pathlib import Path

import pytest

from ofertas import affiliates
from ofertas.config import SCRAPING_TARGETS
from ofertas.scraper import find_next_page_url, full_size_ml_image, parse_listing

FIXTURE = Path(__file__).parent / "fixtures" / "listagem_ml.html"
PAGE_URL = "https://lista.mercadolivre.com.br/informatica/_DisplayType_LF_NoIndex_True"


@pytest.fixture
def offers(monkeypatch):
    monkeypatch.setattr(affiliates, "AFFILIATE_CONFIG", {})
    html = FIXTURE.read_text(encoding="utf-8")
    return parse_listing(html, SCRAPING_TARGETS[0], PAGE_URL)


def test_ignora_patrocinado_e_produto_fora_do_tema(offers):
    titles = [o["title"] for o in offers]
    assert titles == [
        "Notebook Gamer RTX 4060 16GB RAM SSD 512GB",
        "Smartphone Motorola Moto G85 5G 256GB",
    ]


def test_preco_atual_com_centavos_e_nao_o_riscado(offers):
    notebook = offers[0]
    assert notebook["price"] == "R$ 5.499,90"
    assert notebook["original_price"] == "R$ 7.999,00"
    assert notebook["discount"] == "31% OFF"


def test_sem_desconto_nao_mostra_preco_antigo(offers):
    celular = offers[1]
    assert celular["price"] == "R$ 1.299,00"
    assert celular["original_price"] is None
    assert not celular.get("discount")


def test_link_do_produto_sem_rastreio(offers):
    assert offers[0]["link"] == (
        "https://produto.mercadolivre.com.br/MLB-5331114210-notebook-gamer-rtx-4060-16gb-ram-_JM"
    )
    assert offers[1]["link"] == (
        "https://www.mercadolivre.com.br/smartphone-motorola-moto-g85-5g-256gb/p/MLB40274355"
    )


def test_imagem_grande_em_jpeg(offers):
    assert offers[0]["image_url"] == (
        "https://http2.mlstatic.com/D_NQ_NP_900577-MLB97918475120_112025-O.jpg"
    )
    assert offers[1]["image_url"] == (
        "https://http2.mlstatic.com/D_NQ_NP_917764-MLA99509008220_112025-O.jpg"
    )


def test_imagem_fora_do_mlstatic_nao_muda():
    url = "https://outra-cdn.com/foto.webp"
    assert full_size_ml_image(url) == url


def test_proxima_pagina_vem_do_botao_seguinte():
    html = FIXTURE.read_text(encoding="utf-8")
    assert find_next_page_url(html, PAGE_URL) == (
        "https://lista.mercadolivre.com.br/informatica/_Desde_49_DisplayType_LF_NoIndex_True"
    )


def test_ultima_pagina_nao_tem_proxima():
    html = """
    <ul>
      <li class="andes-pagination__button andes-pagination__button--next andes-pagination__button--disabled">
        <a href="#">Seguinte</a>
      </li>
    </ul>
    """
    assert find_next_page_url(html, PAGE_URL) is None
    assert find_next_page_url("<html></html>", PAGE_URL) is None
