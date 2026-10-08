import pytest

from ofertas.prices import calculate_discount, clean_price, format_brl, parse_brl


@pytest.mark.parametrize("texto, esperado", [
    ("210", 210.0),
    ("1.299", 1299.0),
    ("R$ 1.299,90", 1299.9),
    ("12.345.678", 12345678.0),
    ("R$ 99,9", 99.9),
    ("", None),
    ("Grátis", None),
])
def test_parse_brl(texto, esperado):
    assert parse_brl(texto) == esperado


def test_format_brl():
    assert format_brl(1299.9) == "R$ 1.299,90"
    assert format_brl(210.24) == "R$ 210,24"
    assert format_brl(1234567) == "R$ 1.234.567,00"


def test_clean_price():
    assert clean_price("1.299") == "R$ 1.299,00"
    assert clean_price("sem preço") == "Consultar"


def test_desconto_simples():
    assert calculate_discount("R$ 399,00", "R$ 210,24") == "47% OFF"


def test_desconto_cruzando_mil_reais():
    # Antes "1.200" virava 1.2 e "999" ficava 999: o desconto sumia
    assert calculate_discount(clean_price("1.200"), clean_price("999")) == "16% OFF"


def test_sem_desconto_quando_preco_nao_caiu():
    assert calculate_discount("R$ 100,00", "R$ 100,00") is None
    assert calculate_discount("R$ 100,00", "R$ 150,00") is None
    assert calculate_discount("Consultar", "R$ 10,00") is None
