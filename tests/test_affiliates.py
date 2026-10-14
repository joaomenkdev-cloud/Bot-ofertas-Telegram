from ofertas import affiliates

ML = "https://produto.mercadolivre.com.br/MLB-123-mouse-gamer_JM"


def test_sem_afiliado_devolve_o_link_do_produto(monkeypatch):
    monkeypatch.setattr(affiliates, "AFFILIATE_CONFIG", {"mercadolivre": {"params": ""}})
    assert affiliates.create_affiliate_link(ML) == ML
    assert not affiliates.is_affiliate_configured("mercadolivre")


def test_cada_produto_mantem_o_proprio_link(monkeypatch):
    monkeypatch.setattr(
        affiliates, "AFFILIATE_CONFIG", {"mercadolivre": {"params": "matt_tool=1&matt_word=joao"}}
    )
    outro = "https://www.mercadolivre.com.br/teclado/p/MLB999"
    assert affiliates.create_affiliate_link(ML) == ML + "?matt_tool=1&matt_word=joao"
    assert affiliates.create_affiliate_link(outro) == outro + "?matt_tool=1&matt_word=joao"


def test_preserva_query_e_fragmento(monkeypatch):
    monkeypatch.setattr(affiliates, "AFFILIATE_CONFIG", {"amazon": {"params": "tag=meu-20"}})
    link = "https://www.amazon.com.br/dp/B0TESTE?th=1#reviews"
    assert affiliates.create_affiliate_link(link) == "https://www.amazon.com.br/dp/B0TESTE?th=1&tag=meu-20#reviews"


def test_plataforma_desconhecida_nao_muda(monkeypatch):
    monkeypatch.setattr(affiliates, "AFFILIATE_CONFIG", {"amazon": {"params": "tag=meu-20"}})
    link = "https://loja-qualquer.com/produto"
    assert affiliates.create_affiliate_link(link) == link
