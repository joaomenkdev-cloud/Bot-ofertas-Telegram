-- Cria o banco de dados
CREATE DATABASE bot_ofertas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Seleciona o banco
USE bot_ofertas;

-- Cria a tabela de ofertas enviadas
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

-- Verifica se foi criado
SHOW TABLES;
DESCRIBE ofertas_enviadas;