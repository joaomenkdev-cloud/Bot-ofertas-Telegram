# 🤖 Bot de Ofertas do Telegram

Bot inteligente para Telegram que realiza web scraping automático de ofertas no Mercado Livre, filtra produtos de tecnologia e gaming, e envia automaticamente para grupos do Telegram com sistema de fila inteligente para evitar spam.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 📋 Índice

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Estrutura do Banco de Dados](#-estrutura-do-banco-de-dados)
- [Personalização](#-personalização)
- [Comandos do Bot](#-comandos-do-bot)
- [Funcionamento](#-funcionamento)
- [Tecnologias](#-tecnologias)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

## ✨ Características

### 🎯 Sistema Inteligente de Fila
- **Busca contínua**: Procura ofertas até encontrar produtos novos
- **Sistema de fila**: Envia 1 oferta por categoria e armazena o resto
- **Envio programado**: Distribui ofertas a cada 10 minutos automaticamente
- **Anti-duplicatas**: Nunca envia a mesma oferta duas vezes usando hash SHA256

### 🔍 Web Scraping Avançado
- **Múltiplas páginas**: Busca em até 5 páginas por tentativa
- **Seletores inteligentes**: Detecta automaticamente mudanças no HTML
- **Captura de imagens**: Sistema robusto com 3 métodos diferentes
- **Otimização de imagens**: Converte automaticamente para alta resolução

### 🎮 Filtros Personalizados
Aceita apenas produtos de:
- 🖥️ **PC/Setup**: Processadores, RAM, SSD, GPU, monitores, periféricos
- 📱 **Celulares e Tablets**: iPhone, Galaxy, Xiaomi, iPad
- 📺 **TVs**: Smart TV, OLED, QLED, 4K, 8K
- 🎮 **Consoles**: PlayStation, Xbox, Nintendo Switch
- 🪑 **Ergonomia**: Cadeiras gamer, mesas, iluminação

Bloqueia automaticamente: roupas, livros, alimentos, eletrodomésticos, etc.

### 💾 Banco de Dados MySQL
- Armazena histórico de ofertas enviadas
- Sistema de fila com persistência
- Estatísticas completas por fonte
- Limpeza automática de ofertas antigas

## 📦 Requisitos

- **Python 3.8+**
- **Google Chrome** instalado
- **MySQL 8.0+** (ou MariaDB 10.5+)
- **Conexão com internet** estável

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/bot-ofertas-telegram.git
cd bot-ofertas-telegram
```

### 2. Instale as dependências

```bash
pip install python-telegram-bot selenium webdriver-manager beautifulsoup4 lxml mysql-connector-python
```

### 3. Configure o MySQL

Abra o MySQL e execute:

```sql
CREATE DATABASE bot_ofertas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bot_ofertas;

CREATE TABLE ofertas_enviadas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hash_oferta VARCHAR(64) UNIQUE NOT NULL,
    titulo VARCHAR(500) NOT NULL,
    preco VARCHAR(50),
    link TEXT NOT NULL,
    fonte VARCHAR(100),
    data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_hash (hash_oferta),
    INDEX idx_data (data_envio)
);

CREATE TABLE fila_ofertas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hash_oferta VARCHAR(64) UNIQUE NOT NULL,
    dados_oferta TEXT NOT NULL,
    fonte VARCHAR(100),
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_fonte (fonte),
    INDEX idx_data (data_criacao)
);
```

## ⚙️ Configuração

### 1. Crie um Bot no Telegram

1. Abra o Telegram e procure por `@BotFather`
2. Envie `/newbot` e siga as instruções
3. Copie o **token** fornecido

### 2. Descubra o ID do seu grupo

1. Adicione o bot `@getmyid_bot` ao seu grupo
2. Ele enviará o **ID do grupo** (começa com `-`)
3. Remova o bot depois

### 3. Configure o arquivo `bot.py`

Edite as seguintes linhas no arquivo:

```python
# Token do Bot
BOT_TOKEN = "seu-token-aqui"

# ID do Grupo
GROUP_CHAT_ID = "-1001234567890"

# Credenciais do MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sua-senha-mysql',
    'database': 'bot_ofertas'
}
```

### 4. (Opcional) Configure seu link de afiliado

```python
def create_affiliate_link(original_link):
    # Adicione sua lógica de afiliado aqui
    # Exemplo para Amazon:
    if 'amazon.com' in original_link:
        separator = '&' if '?' in original_link else '?'
        return f"{original_link}{separator}tag=seu-id-20"
    
    return original_link
```

## 🎮 Uso

### Iniciar o bot

```bash
python bot.py
```

Você verá:

```
============================================================
🤖 BOT DE OFERTAS COM FILA INTELIGENTE
============================================================
📅 Iniciado: 10/12/2025 às 14:30:00
🔍 Sites: 5
============================================================

🗄️ Inicializando banco de dados MySQL...
✅ Banco de dados 'bot_ofertas' verificado/criado
✅ Tabelas verificadas/criadas

✅ Bot iniciado com sistema de fila!
⏰ Envio da fila: a cada 10 minutos
🔄 Verificação: a cada 30 minutos
```

### Busca Manual

No Telegram, envie:

```
/buscar
```

O bot buscará ofertas imediatamente.

## 📊 Estrutura do Banco de Dados

### Tabela: `ofertas_enviadas`

Armazena todas as ofertas já enviadas para evitar duplicatas.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT | ID auto-incremento |
| hash_oferta | VARCHAR(64) | Hash único SHA256 da oferta |
| titulo | VARCHAR(500) | Título do produto |
| preco | VARCHAR(50) | Preço formatado |
| link | TEXT | URL do produto |
| fonte | VARCHAR(100) | Nome da fonte (categoria) |
| data_envio | DATETIME | Data/hora do envio |

### Tabela: `fila_ofertas`

Armazena ofertas aguardando envio.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT | ID auto-incremento |
| hash_oferta | VARCHAR(64) | Hash único da oferta |
| dados_oferta | TEXT | JSON com dados completos |
| fonte | VARCHAR(100) | Nome da fonte |
| data_criacao | DATETIME | Data/hora de criação |

## 🎨 Personalização

### Adicionar novas categorias

Edite `SCRAPING_TARGETS`:

```python
SCRAPING_TARGETS = [
    {
        "name": "Nome da Categoria",
        "url": "https://url-do-mercado-livre.com.br",
        "selectors": {
            "container": ".classe-container",
            "title": ".classe-titulo",
            "price": ".classe-preco",
            "link": ".classe-link",
            "image": ".classe-imagem"
        }
    },
]
```

### Modificar palavras-chave

Edite as listas `ALLOWED_KEYWORDS` e `BLOCKED_KEYWORDS`:

```python
ALLOWED_KEYWORDS = [
    'seu', 'produto', 'aqui',
]

BLOCKED_KEYWORDS = [
    'produto', 'bloqueado',
]
```

### Alterar intervalo de envio

No `main()`:

```python
# Envia a cada 5 minutos (300 segundos)
application.job_queue.run_repeating(send_queued_offers, interval=300, first=30)

# Verifica a cada 15 minutos (900 segundos)
application.job_queue.run_repeating(check_and_search_if_needed, interval=900, first=60)
```

## 🎯 Comandos do Bot

| Comando | Descrição |
|---------|-----------|
| `/buscar` | Busca ofertas imediatamente |
| `/status` | Mostra estatísticas e fila |

### Exemplo de `/status`

```
🤖 Status do Bot

✅ Bot ativo
🔍 Sites: 5

📊 Estatísticas:
📦 Total enviadas: 1,234
📅 Hoje: 45

📥 Fila de ofertas:
Total na fila: 87
  • Mercado Livre - Informática: 23
  • Mercado Livre - Celulares: 18
  • Mercado Livre - TVs: 15
  • Mercado Livre - Consoles: 31
```

## 🔄 Funcionamento

### Fluxo de Busca

```
1. Bot inicia busca
   ↓
2. Acessa categoria (ex: Informática)
   ↓
3. Faz scraping de até 5 páginas
   ↓
4. Filtra por palavras-chave
   ↓
5. Remove duplicatas (verifica hash no BD)
   ↓
6. Envia PRIMEIRA oferta nova
   ↓
7. Armazena RESTO na fila
   ↓
8. Repete para próxima categoria
```

### Sistema de Fila

```
A cada 10 minutos:
   ↓
Pega 1 oferta de cada categoria da fila
   ↓
Envia para o grupo
   ↓
Remove da fila e salva em ofertas_enviadas
```

### Verificação Automática

```
A cada 30 minutos:
   ↓
Verifica quantidade na fila
   ↓
Se < 5 ofertas → Busca novas automaticamente
```

## 🛠️ Tecnologias

- **[Python](https://www.python.org/)** - Linguagem principal
- **[python-telegram-bot](https://python-telegram-bot.org/)** - API do Telegram
- **[Selenium](https://www.selenium.dev/)** - Automação do navegador
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** - Parser de HTML
- **[MySQL](https://www.mysql.com/)** - Banco de dados
- **[WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)** - Gerenciamento do ChromeDriver

## 🐛 Solução de Problemas

### Erro: "Can't connect to MySQL server"

**Solução**: Verifique se o MySQL está rodando:

```bash
# Windows
services.msc → procure por MySQL

# Linux/Mac
sudo systemctl status mysql
```

### Erro: "ChromeDriver not found"

**Solução**: Certifique-se de que o Google Chrome está instalado. O WebDriver Manager baixa automaticamente o driver correto.

### Bot não envia imagens

**Solução**: O código está configurado sem `--headless`. Se quiser modo invisível, comente a linha:

```python
# chrome_options.add_argument('--headless')
```

### Todas as ofertas são duplicadas

**Solução**: Limpe o banco de dados:

```sql
TRUNCATE TABLE ofertas_enviadas;
TRUNCATE TABLE fila_ofertas;
```

## 🤝 Contribuindo

Contribuições são bem-vindas! 

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ⚠️ Aviso Legal

Este bot é fornecido apenas para fins educacionais. Certifique-se de:

- ✅ Respeitar os **Termos de Serviço** do Mercado Livre
- ✅ Não sobrecarregar servidores com requisições excessivas
- ✅ Usar **links de afiliado autorizados** apenas
- ✅ Respeitar a **política de privacidade** dos usuários

O uso inadequado desta ferramenta é de **responsabilidade exclusiva do usuário**.

---



**Desenvolvido com ❤️ para encontrar as melhores ofertas!**

⭐ Se este projeto te ajudou, deixe uma estrela!

