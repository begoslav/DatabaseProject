-- E-shop Database Schema
-- MySQL 5.7+

CREATE DATABASE IF NOT EXISTS eshop;
USE eshop;

-- ============================================
-- TABULKA: kategorie
-- ============================================
CREATE TABLE kategorie (
    id_kategorie INT PRIMARY KEY AUTO_INCREMENT,
    nazev VARCHAR(100) NOT NULL UNIQUE,
    popis VARCHAR(255),
    je_aktivni BOOLEAN NOT NULL DEFAULT TRUE,
    vytvoren TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABULKA: produkty
-- ============================================
CREATE TABLE produkty (
    id_produktu INT PRIMARY KEY AUTO_INCREMENT,
    nazev VARCHAR(150) NOT NULL,
    popis TEXT,
    cena_bez_dph DECIMAL(10, 2) NOT NULL,
    sazba_dph DECIMAL(5, 2) NOT NULL DEFAULT 21.00,
    skladem INT NOT NULL DEFAULT 0,
    typ_produktu ENUM('fyzicka', 'digitalni', 'sluzba') NOT NULL DEFAULT 'fyzicka',
    je_aktivni BOOLEAN NOT NULL DEFAULT TRUE,
    vytvoreno DATETIME DEFAULT CURRENT_TIMESTAMP,
    aktualizovano DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABULKA: produkt_kategorie (M:N vazba)
-- ============================================
CREATE TABLE produkt_kategorie (
    id_produktu INT NOT NULL,
    id_kategorie INT NOT NULL,
    PRIMARY KEY (id_produktu, id_kategorie),
    FOREIGN KEY (id_produktu) REFERENCES produkty(id_produktu) ON DELETE CASCADE,
    FOREIGN KEY (id_kategorie) REFERENCES kategorie(id_kategorie) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABULKA: zakaznici
-- ============================================
CREATE TABLE zakaznici (
    id_zakaznika INT PRIMARY KEY AUTO_INCREMENT,
    jmeno VARCHAR(100) NOT NULL,
    prijmeni VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefon VARCHAR(20),
    adresa VARCHAR(255) NOT NULL,
    mesto VARCHAR(100) NOT NULL,
    psc VARCHAR(10) NOT NULL,
    stav VARCHAR(100),
    zeme VARCHAR(100) DEFAULT 'Česká republika',
    registrovan DATETIME DEFAULT CURRENT_TIMESTAMP,
    posledni_pristup DATETIME,
    je_aktivni BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABULKA: objednavky
-- ============================================
CREATE TABLE objednavky (
    id_objednavky INT PRIMARY KEY AUTO_INCREMENT,
    id_zakaznika INT NOT NULL,
    casova_znamka_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP,
    casova_znamka_posledni_zmena DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    stav ENUM('nova', 'potvrzena', 'zaplacena', 'vyrazena', 'dorucena', 'zrusena') NOT NULL DEFAULT 'nova',
    poznamka TEXT,
    cena_bez_dph DECIMAL(12, 2) NOT NULL DEFAULT 0,
    sazba_dph DECIMAL(5, 2) NOT NULL DEFAULT 21.00,
    cena_s_dph DECIMAL(12, 2) NOT NULL DEFAULT 0,
    FOREIGN KEY (id_zakaznika) REFERENCES zakaznici(id_zakaznika) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABULKA: polozky_objednavek
-- ============================================
CREATE TABLE polozky_objednavek (
    id_polozky INT PRIMARY KEY AUTO_INCREMENT,
    id_objednavky INT NOT NULL,
    id_produktu INT NOT NULL,
    pocet INT NOT NULL CHECK (pocet > 0),
    jednotkova_cena DECIMAL(10, 2) NOT NULL,
    sleva_procenta DECIMAL(5, 2) NOT NULL DEFAULT 0,
    FOREIGN KEY (id_objednavky) REFERENCES objednavky(id_objednavky) ON DELETE CASCADE,
    FOREIGN KEY (id_produktu) REFERENCES produkty(id_produktu) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- VIEW: v_objednavky_s_detaily
-- ============================================
CREATE OR REPLACE VIEW v_objednavky_s_detaily AS
SELECT 
    o.id_objednavky,
    o.id_zakaznika,
    CONCAT(z.jmeno, ' ', z.prijmeni) AS zakaznik,
    z.email,
    o.casova_znamka_vytvoreni,
    o.stav,
    COUNT(po.id_polozky) AS pocet_polozek,
    SUM(po.pocet) AS celkovy_pocet_kusu,
    o.cena_s_dph AS celkova_cena
FROM objednavky o
JOIN zakaznici z ON o.id_zakaznika = z.id_zakaznika
LEFT JOIN polozky_objednavek po ON o.id_objednavky = po.id_objednavky
GROUP BY o.id_objednavky;

-- ============================================
-- VIEW: v_skladova_dostupnost
-- ============================================
CREATE OR REPLACE VIEW v_skladova_dostupnost AS
SELECT 
    p.id_produktu,
    p.nazev,
    p.cena_bez_dph,
    p.cena_bez_dph * (1 + p.sazba_dph / 100) AS cena_s_dph,
    p.skladem,
    GROUP_CONCAT(k.nazev SEPARATOR ', ') AS kategorie,
    CASE 
        WHEN p.skladem = 0 THEN 'vyprodáno'
        WHEN p.skladem < 5 THEN 'nízký'
        WHEN p.skladem < 20 THEN 'střední'
        ELSE 'vysoký'
    END AS dostupnost
FROM produkty p
LEFT JOIN produkt_kategorie pk ON p.id_produktu = pk.id_produktu
LEFT JOIN kategorie k ON pk.id_kategorie = k.id_kategorie
WHERE p.je_aktivni = TRUE
GROUP BY p.id_produktu;

-- ============================================
-- INDEXY pro optimalizaci
-- ============================================
CREATE INDEX idx_zakaznici_email ON zakaznici(email);
CREATE INDEX idx_zakaznici_je_aktivni ON zakaznici(je_aktivni);
CREATE INDEX idx_produkty_typ ON produkty(typ_produktu);
CREATE INDEX idx_produkty_je_aktivni ON produkty(je_aktivni);
CREATE INDEX idx_objednavky_zakaznika ON objednavky(id_zakaznika);
CREATE INDEX idx_objednavky_stav ON objednavky(stav);
CREATE INDEX idx_objednavky_casova_znamka ON objednavky(casova_znamka_vytvoreni);
CREATE INDEX idx_polozky_objednavky ON polozky_objednavek(id_objednavky);
CREATE INDEX idx_polozky_produktu ON polozky_objednavek(id_produktu);
