CREATE DATABASE IF NOT EXISTS CryptoPunksChatDB DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE CryptoPunksChatDB;

CREATE TABLE IF NOT EXISTS clients (
    id INT(10) NOT NULL,
    clientname VARCHAR(50) NOT NULL,
    passwordhash VARBINARY(32) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phonenumber VARCHAR(20),
    role VARCHAR(20) NOT NULL DEFAULT 'client',
    hexcolor VARCHAR(7) NOT NULL DEFAULT '#14c400',

    PRIMARY KEY (id)
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- DESCRIBE clients; - показать поля таблицы
-- DROP DATABASE db_name; - удалить базу данных

-- ALTER TABLE Clients
-- ADD COLUMN user_color varchar(7); - добавить колонку в БД
