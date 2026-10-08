# 🤖 Bot de Ofertas — Mercado Livre → Telegram

Bot que raspa ofertas de tecnologia e gaming do Mercado Livre (informática, componentes,
celulares, TVs e consoles) e posta no seu grupo/canal do Telegram, sem repetir ofertas.

## ✨ Como funciona

- Abre as listagens com Selenium, lê os cards (`poly-card`) e guarda o **preço atual**, o preço
  antigo e o desconto.
- Filtra por palavras-chave (aceita/bloqueia por palavra inteira) e ignora anúncios patrocinados.
- Posta **uma oferta por vez** com foto, no ritmo de **12/hora nos horários de pico** e
  **6/hora nos demais**, alternando entre as categorias.
- Histórico e fila ficam em um arquivo **SQLite** (`ofertas.db`), criado sozinho.
- **Afiliado é opcional**: sem configurar, o bot envia o link normal do produto.

## 🚀 Como rodar

Requisitos: Python 3.10+ e Google Chrome.

```bash
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

copy .env.example .env          # Linux/macOS: cp .env.example .env
# edite o .env (token, grupo, admins)

python bot.py
```

### Configuração (`.env`)

| Variável | Obrigatória | Para quê |
|---|---|---|
| `BOT_TOKEN` | sim | Token do bot (@BotFather → `/newbot`) |
| `GROUP_CHAT_ID` | sim | ID do grupo/canal onde postar (começa com `-100`) |
| `ADMIN_IDS` | recomendada | IDs de quem pode usar `/buscar`, `/status`, `/config` |
| `ML_AFFILIATE_PARAMS` | não | Parâmetros de afiliado do ML, acrescentados ao link de cada produto |
| `AMAZON_AFFILIATE_TAG` | não | Tag do Amazon Associados |
| `DB_PATH` | não | Caminho do SQLite (padrão: `ofertas.db`) |

> ⚠️ O `.env` não vai para o git. Nunca coloque o token no código.

### Comandos (só para `ADMIN_IDS`)

- `/buscar` — busca ofertas agora
- `/status` — estatísticas e fila
- `/config` — mostra o estado da configuração de afiliados

## ⚠️ Mercado Livre pode pedir login

Dependendo da rede e do momento, o Mercado Livre redireciona o navegador automatizado para uma
tela de **"acesse sua conta"** (`/gz/account-verification`) antes de mostrar as listagens. Quando
isso acontece, o bot avisa no log e **não contorna** a barreira. Se isso for constante no seu
ambiente, a alternativa estável é usar a [API oficial do Mercado Livre](https://developers.mercadolivre.com.br/).

## 📁 Estrutura

```
bot.py                  # ponto de entrada: monta o bot e agenda os jobs
ofertas/
  config.py             # .env, filtros de palavras-chave, listagens e seletores
  scraper.py            # Selenium + BeautifulSoup (parser, paginação, imagens)
  jobs.py               # busca, fila e envio no ritmo do horário
  sender.py             # mensagem em HTML para o Telegram
  database.py           # SQLite: ofertas enviadas e fila
  filters.py            # filtro por palavra inteira
  prices.py             # preços em BRL e desconto
  affiliates.py         # parâmetros de afiliado
  commands.py           # comandos de admin
  scheduling.py         # ofertas por hora (pico / normal)
tests/                  # pytest
```

## 🧪 Testes

```bash
pip install -r requirements-dev.txt
pytest
```

## 📝 Licença

MIT — veja [LICENSE](LICENSE).
