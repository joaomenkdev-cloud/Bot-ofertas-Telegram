"""Persistência: ofertas já enviadas e fila de envio (SQLite)."""

import hashlib
import json
import sqlite3
from contextlib import closing

from .affiliates import detect_platform
from .config import DB_PATH

# ═════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DO BANCO DE DADOS
# ═════════════════════════════════════════════════════════════════════════════

def create_database_connection():
    """Abre conexão com o arquivo SQLite (criado automaticamente se não existir)"""
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as e:
        print(f"❌ Erro ao abrir o banco SQLite em {DB_PATH}: {e}")
        return None

def initialize_database():
    """Cria as tabelas se não existirem"""
    connection = create_database_connection()
    if not connection:
        return
    try:
        with closing(connection), connection:
            # Tabela de ofertas enviadas (evita duplicatas)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS ofertas_enviadas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hash_oferta TEXT UNIQUE NOT NULL,
                    titulo TEXT NOT NULL,
                    preco TEXT,
                    link TEXT NOT NULL,
                    fonte TEXT,
                    plataforma TEXT,
                    tem_afiliado INTEGER DEFAULT 0,
                    data_envio TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_enviadas_data ON ofertas_enviadas (data_envio)"
            )

            # Tabela de fila de ofertas
            connection.execute("""
                CREATE TABLE IF NOT EXISTS fila_ofertas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hash_oferta TEXT UNIQUE NOT NULL,
                    dados_oferta TEXT NOT NULL,
                    fonte TEXT,
                    plataforma TEXT,
                    data_criacao TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_fila_fonte ON fila_ofertas (fonte, id)"
            )
        print(f"✅ Banco SQLite pronto: {DB_PATH}")
    except sqlite3.Error as e:
        print(f"❌ Erro ao inicializar banco: {e}")

def generate_offer_hash(title, link):
    """Gera um hash único para cada oferta (evita duplicatas)"""
    clean_link = link.split('?')[0].split('#')[0]
    offer_string = f"{title.lower().strip()}|{clean_link}"
    return hashlib.sha256(offer_string.encode()).hexdigest()

def is_offer_already_sent(offer_hash):
    """Verifica se a oferta já foi enviada antes"""
    connection = create_database_connection()
    if not connection:
        return False
    try:
        with closing(connection):
            result = connection.execute(
                "SELECT id FROM ofertas_enviadas WHERE hash_oferta = ?", (offer_hash,)
            ).fetchone()
        return result is not None
    except sqlite3.Error as e:
        print(f"❌ Erro ao verificar oferta: {e}")
        return False

def save_sent_offer(offer):
    """Salva oferta no banco após enviar"""
    connection = create_database_connection()
    if not connection:
        return False
    try:
        offer_hash = generate_offer_hash(offer['title'], offer['link'])
        platform = detect_platform(offer['link'])
        has_affiliate = offer.get('has_affiliate', False)

        with closing(connection), connection:
            connection.execute("""
                INSERT INTO ofertas_enviadas (hash_oferta, titulo, preco, link, fonte, plataforma, tem_afiliado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (offer_hash, offer['title'][:500], offer['price'], offer['link'],
                  offer['source'], platform, has_affiliate))
        return True
    except sqlite3.Error as e:
        print(f"❌ Erro ao salvar oferta: {e}")
        return False

def add_to_queue(offer):
    """Adiciona oferta à fila para envio posterior"""
    connection = create_database_connection()
    if not connection:
        return False
    try:
        offer_hash = generate_offer_hash(offer['title'], offer['link'])
        dados_json = json.dumps(offer)
        platform = detect_platform(offer['link'])

        with closing(connection), connection:
            connection.execute("""
                INSERT OR IGNORE INTO fila_ofertas (hash_oferta, dados_oferta, fonte, plataforma)
                VALUES (?, ?, ?, ?)
            """, (offer_hash, dados_json, offer['source'], platform))
        return True
    except sqlite3.Error as e:
        print(f"❌ Erro ao adicionar à fila: {e}")
        return False

def get_next_offer_from_queue(source):
    """Pega (e remove) a próxima oferta da fila"""
    connection = create_database_connection()
    if not connection:
        return None
    try:
        with closing(connection), connection:
            result = connection.execute("""
                SELECT id, dados_oferta
                FROM fila_ofertas
                WHERE fonte = ?
                ORDER BY id ASC
                LIMIT 1
            """, (source,)).fetchone()

            if not result:
                return None

            connection.execute("DELETE FROM fila_ofertas WHERE id = ?", (result['id'],))
        return json.loads(result['dados_oferta'])
    except sqlite3.Error as e:
        print(f"❌ Erro ao buscar da fila: {e}")
        return None

def get_queue_count():
    """Retorna quantidade de ofertas na fila"""
    connection = create_database_connection()
    if not connection:
        return {}
    try:
        with closing(connection):
            results = connection.execute("""
                SELECT fonte, COUNT(*) AS quantidade
                FROM fila_ofertas
                GROUP BY fonte
            """).fetchall()
        return {r['fonte']: r['quantidade'] for r in results}
    except sqlite3.Error as e:
        print(f"❌ Erro ao contar fila: {e}")
        return {}

def get_statistics():
    """Retorna estatísticas do bot"""
    connection = create_database_connection()
    if not connection:
        return None
    try:
        with closing(connection):
            # Total de ofertas
            total = connection.execute(
                "SELECT COUNT(*) FROM ofertas_enviadas"
            ).fetchone()[0]

            # Ofertas de hoje (data_envio fica em UTC; compara no horário local)
            hoje = connection.execute("""
                SELECT COUNT(*)
                FROM ofertas_enviadas
                WHERE DATE(data_envio, 'localtime') = DATE('now', 'localtime')
            """).fetchone()[0]

            # Por fonte
            por_fonte = [dict(r) for r in connection.execute("""
                SELECT fonte, COUNT(*) AS quantidade
                FROM ofertas_enviadas
                GROUP BY fonte
                ORDER BY quantidade DESC
            """)]

            # Estatísticas de afiliados
            com_afiliado = connection.execute(
                "SELECT COUNT(*) FROM ofertas_enviadas WHERE tem_afiliado = 1"
            ).fetchone()[0]

        return {
            'total': total,
            'hoje': hoje,
            'por_fonte': por_fonte,
            'com_afiliado': com_afiliado,
            'sem_afiliado': total - com_afiliado
        }
    except sqlite3.Error as e:
        print(f"❌ Erro ao buscar estatísticas: {e}")
        return None
