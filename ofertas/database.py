"""Persistência: ofertas já enviadas e fila de envio."""

import hashlib
import json

import mysql.connector
from mysql.connector import Error

from .affiliates import detect_platform
from .config import DB_CONFIG

# ═════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DO BANCO DE DADOS
# ═════════════════════════════════════════════════════════════════════════════

def create_database_connection():
    """Cria conexão com o banco de dados MySQL"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        print(f"💡 Verifique se o MySQL está rodando e se a senha está correta")
        return None

def initialize_database():
    """Cria o banco e as tabelas se não existirem"""
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        
        # Cria o banco
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"✅ Banco de dados '{DB_CONFIG['database']}' verificado/criado")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Tabela de ofertas enviadas (evita duplicatas)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ofertas_enviadas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hash_oferta VARCHAR(64) UNIQUE NOT NULL,
                titulo VARCHAR(500) NOT NULL,
                preco VARCHAR(50),
                link TEXT NOT NULL,
                fonte VARCHAR(100),
                plataforma VARCHAR(50),
                tem_afiliado BOOLEAN DEFAULT FALSE,
                data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_hash (hash_oferta),
                INDEX idx_data (data_envio),
                INDEX idx_plataforma (plataforma)
            )
        """)
        
        # Tabela de fila de ofertas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fila_ofertas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hash_oferta VARCHAR(64) UNIQUE NOT NULL,
                dados_oferta TEXT NOT NULL,
                fonte VARCHAR(100),
                plataforma VARCHAR(50),
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_fonte (fonte),
                INDEX idx_data (data_criacao),
                INDEX idx_plataforma (plataforma)
            )
        """)
        
        print("✅ Tabelas verificadas/criadas")
        cursor.close()
        connection.close()
    except Error as e:
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
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM ofertas_enviadas WHERE hash_oferta = %s", (offer_hash,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None
    except Error as e:
        print(f"❌ Erro ao verificar oferta: {e}")
        return False

def save_sent_offer(offer):
    """Salva oferta no banco após enviar"""
    connection = create_database_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        offer_hash = generate_offer_hash(offer['title'], offer['link'])
        platform = detect_platform(offer['link'])
        has_affiliate = offer.get('has_affiliate', False)
        
        cursor.execute("""
            INSERT INTO ofertas_enviadas (hash_oferta, titulo, preco, link, fonte, plataforma, tem_afiliado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (offer_hash, offer['title'][:500], offer['price'], offer['link'], 
              offer['source'], platform, has_affiliate))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"❌ Erro ao salvar oferta: {e}")
        return False

def add_to_queue(offer):
    """Adiciona oferta à fila para envio posterior"""
    connection = create_database_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        offer_hash = generate_offer_hash(offer['title'], offer['link'])
        dados_json = json.dumps(offer)
        platform = detect_platform(offer['link'])
        
        cursor.execute("""
            INSERT IGNORE INTO fila_ofertas (hash_oferta, dados_oferta, fonte, plataforma)
            VALUES (%s, %s, %s, %s)
        """, (offer_hash, dados_json, offer['source'], platform))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"❌ Erro ao adicionar à fila: {e}")
        return False

def get_next_offer_from_queue(source):
    """Pega a próxima oferta da fila"""
    connection = create_database_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, hash_oferta, dados_oferta 
            FROM fila_ofertas 
            WHERE fonte = %s 
            ORDER BY data_criacao ASC 
            LIMIT 1
        """, (source,))
        result = cursor.fetchone()
        
        if result:
            cursor.execute("DELETE FROM fila_ofertas WHERE id = %s", (result['id'],))
            connection.commit()
            cursor.close()
            connection.close()
            return json.loads(result['dados_oferta'])
        
        cursor.close()
        connection.close()
        return None
    except Error as e:
        print(f"❌ Erro ao buscar da fila: {e}")
        return None

def get_queue_count():
    """Retorna quantidade de ofertas na fila"""
    connection = create_database_connection()
    if not connection:
        return {}
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT fonte, COUNT(*) as quantidade 
            FROM fila_ofertas 
            GROUP BY fonte
        """)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return {r['fonte']: r['quantidade'] for r in results}
    except Error as e:
        print(f"❌ Erro ao contar fila: {e}")
        return {}

def get_statistics():
    """Retorna estatísticas do bot"""
    connection = create_database_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Total de ofertas
        cursor.execute("SELECT COUNT(*) as total FROM ofertas_enviadas")
        total = cursor.fetchone()['total']
        
        # Ofertas de hoje
        cursor.execute("""
            SELECT COUNT(*) as hoje 
            FROM ofertas_enviadas 
            WHERE DATE(data_envio) = CURDATE()
        """)
        hoje = cursor.fetchone()['hoje']
        
        # Por fonte
        cursor.execute("""
            SELECT fonte, COUNT(*) as quantidade 
            FROM ofertas_enviadas 
            GROUP BY fonte 
            ORDER BY quantidade DESC
        """)
        por_fonte = cursor.fetchall()
        
        # Estatísticas de afiliados
        cursor.execute("""
            SELECT 
                COUNT(*) as total_com_afiliado 
            FROM ofertas_enviadas 
            WHERE tem_afiliado = TRUE
        """)
        com_afiliado = cursor.fetchone()['total_com_afiliado']
        
        cursor.close()
        connection.close()
        return {
            'total': total, 
            'hoje': hoje, 
            'por_fonte': por_fonte,
            'com_afiliado': com_afiliado,
            'sem_afiliado': total - com_afiliado
        }
    except Error as e:
        print(f"❌ Erro ao buscar estatísticas: {e}")
        return None
