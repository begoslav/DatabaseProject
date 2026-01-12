-- Vzorová data pro testování
USE eshop;

-- Kategorie
INSERT INTO kategorie (nazev, popis) VALUES
('Elektronika', 'Elektronické zařízení a příslušenství'),
('Knihy', 'Tištěné a digitální knihy'),
('Oblečení', 'Pánské a dámské oblečení'),
('Domácnost', 'Domácí potřeby a vybavení'),
('Sport', 'Sportovní vybavení a oblečení');

-- Produkty
INSERT INTO produkty (nazev, popis, cena_bez_dph, sazba_dph, skladem, typ_produktu) VALUES
('Notebook HP Pavilion', 'Výkonný notebook pro kancelář a zábavu', 22000.00, 21.00, 5, 'fyzicka'),
('Myš bezdrátová Logitech', 'Ergonomická bezdrátová myš', 599.00, 21.00, 50, 'fyzicka'),
('Klávesnice mechanická', 'Gaming klávesnice RGB', 1999.00, 21.00, 15, 'fyzicka'),
('Monitory 27" UHD', '4K monitor s HDR', 8999.00, 21.00, 8, 'fyzicka'),
('USB-C kabel 2m', 'Kvalitní USB-C kabel', 299.00, 21.00, 100, 'fyzicka'),
('Kniha - Python programování', 'Učebnice Pythonu od základů', 450.00, 21.00, 30, 'fyzicka'),
('Tričko bavlněné', 'Pohodlné bavlněné tričko', 299.00, 21.00, 200, 'fyzicka'),
('Tepláky sportovní', 'Pohodlné sportovní tepláky', 799.00, 21.00, 80, 'fyzicka'),
('Polštář paměťový', 'Ortopedický polštář', 1299.00, 21.00, 25, 'fyzicka'),
('Světlo LED 50W', 'Úsporné LED svítidlo', 599.00, 21.00, 0, 'fyzicka');

-- Spojení produktů s kategoriemi (M:N)
INSERT INTO produkt_kategorie (id_produktu, id_kategorie) VALUES
(1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
(6, 2),
(7, 3), (8, 3),
(9, 4), (10, 4);

-- Zákazníci
INSERT INTO zakaznici (jmeno, prijmeni, email, telefon, adresa, mesto, psc, stav, zeme) VALUES
('Jan', 'Novotný', 'jan.novotny@email.com', '732123456', 'Ulice U Parku 123', 'Praha', '110 00', 'Praha', 'Česká republika'),
('Petra', 'Svobodová', 'petra.svobodova@email.com', '720456789', 'Nám. Míru 456', 'Brno', '602 00', 'Jihomoravský', 'Česká republika'),
('David', 'Kučera', 'david.kucera@email.com', '605111222', 'Smetanova 789', 'Ostrava', '702 00', 'Moravskoslezský', 'Česká republika'),
('Marie', 'Pokorná', 'marie.pokorna@email.com', NULL, 'Školní 321', 'Plzeň', '301 00', 'Plzeňský', 'Česká republika'),
('Tomáš', 'Urban', 'tomas.urban@email.com', '774888999', 'Mánesova 555', 'Liberec', '460 01', 'Liberecký', 'Česká republika');

-- Objednávky se vzorová data
INSERT INTO objednavky (id_zakaznika, stav, cena_bez_dph, sazba_dph, cena_s_dph, poznamka) VALUES
(1, 'dorucena', 23599.00, 21.00, 28555.79, 'Doručeno bez problémů'),
(2, 'zaplacena', 1498.00, 21.00, 1812.58, 'Čeká na doručení'),
(1, 'nova', 22999.00, 21.00, 27839.79, 'Nová objednávka'),
(3, 'vyrazena', 3098.00, 21.00, 3748.58, 'Na cestě k zákazníkovi'),
(4, 'potvrzena', 8999.00, 21.00, 10889.79, 'Objednávka potvrzena');

-- Položky objednávek
INSERT INTO polozky_objednavek (id_objednavky, id_produktu, pocet, jednotkova_cena, sleva_procenta) VALUES
(1, 1, 1, 22000.00, 0),
(1, 5, 1, 299.00, 10),
(1, 2, 1, 599.00, 0),
(2, 3, 1, 1999.00, 0),
(2, 2, 1, 599.00, 50),
(3, 4, 1, 8999.00, 0),
(3, 10, 2, 599.00, 0),
(3, 6, 1, 450.00, 0),
(4, 3, 1, 1999.00, 0),
(4, 7, 1, 299.00, 0),
(4, 9, 1, 800.00, 0),
(5, 4, 1, 8999.00, 0);
