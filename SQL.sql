/* TABLA  HECHOS */

DROP TABLE IF EXISTS {martindattoliv_coderhouse}.games;
        CREATE TABLE {martindattoliv_coderhouse}.games(
        id SERIAL PRIMARY KEY,
        slug VARCHAR(255),
        name VARCHAR(255),
        playtime INT,
        released DATE,
        rating FLOAT,
        rating_top INT,
        updated TIMESTAMP,
        platform_ids VARCHAR(255),
        store_ids VARCHAR(255),
        parent_platform_ids VARCHAR(255),
        genre_ids VARCHAR(255)     
    );


'TABLAS DIMENSION'

DROP TABLE IF EXISTS {martindattoliv_coderhouse}.platforms;
        CREATE TABLE {martindattoliv_coderhouse}.platforms(
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        slug VARCHAR(255)         
    );

DROP TABLE IF EXISTS {martindattoliv_coderhouse}.Parent_platforms;
        CREATE TABLE {martindattoliv_coderhouse}.Parent_platforms(
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        slug VARCHAR(255),          
    );

DROP TABLE IF EXISTS {martindattoliv_coderhouse}.store;
        CREATE TABLE {martindattoliv_coderhouse}.store(
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        slug VARCHAR(255),
    );

DROP TABLE IF EXISTS {martindattoliv_coderhouse}.genre;
        CREATE TABLE {martindattoliv_coderhouse}.genre(
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        slug VARCHAR(255),
    );