from ofertas.sender import build_caption


def _offer(**extra):
    offer = {
        "title": "Mouse Gamer *RGB* [Edição_Limitada] <Pro> & Cia",
        "price": "R$ 210,24",
        "link": "https://produto.mercadolivre.com.br/MLB-1?a=1&b=2",
        "source": "Mercado Livre - Informática",
    }
    offer.update(extra)
    return offer


def test_caracteres_especiais_do_titulo_sao_escapados():
    caption = build_caption(_offer())
    assert "<b>Mouse Gamer *RGB* [Edição_Limitada] &lt;Pro&gt; &amp; Cia</b>" in caption


def test_link_com_query_string_fica_valido():
    caption = build_caption(_offer())
    assert '<a href="https://produto.mercadolivre.com.br/MLB-1?a=1&amp;b=2">' in caption


def test_preco_riscado_quando_ha_desconto():
    caption = build_caption(_offer(original_price="R$ 399,00", discount="47% OFF"))
    assert "<s>R$ 399,00</s> ➜ <b>R$ 210,24</b>" in caption
    assert "<b>47% OFF</b>" in caption


def test_sem_desconto_mostra_so_o_preco():
    caption = build_caption(_offer())
    assert "<s>" not in caption
    assert "💰 <b>R$ 210,24</b>" in caption
