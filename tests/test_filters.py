import pytest

from ofertas.filters import contains_keyword, is_pc_related_product


@pytest.mark.parametrize("titulo", [
    "Smartphone Motorola Moto G85 5G 256GB",
    "Power Bank Bateria Externa 20000mAh Xiaomi",
    "Smart TV 50 4K para sua casa",
    "Monitores Gamer 24 Polegadas 165hz",
    "Memória RAM DDR4 16GB 3200MHz",
    "SSD NVMe M.2 1TB",
])
def test_aceita_produtos_de_tecnologia(titulo):
    assert is_pc_related_product(titulo)


@pytest.mark.parametrize("titulo", [
    "Calça Jeans Masculina Original Elastano",
    "Ferofire Atracione Men 50ml Perfume Masculino",
    "Capacete Para Motocicleta Fechado",
    "Bateria Acústica Infantil Completa",
    "Panela de Pressão Tramontina 4,5 Litros",
])
def test_bloqueia_ou_ignora_o_resto(titulo):
    assert not is_pc_related_product(titulo)


def test_palavra_inteira():
    assert not contains_keyword("panela tramontina", "ram")
    assert contains_keyword("memória ram ddr5", "ram")
    assert contains_keyword("kit 2 mouses sem fio", "mouse")
    assert contains_keyword("cabo hdmi 2.1", "cabo hdmi")
    assert not contains_keyword("cabo hdmi", "hd")
