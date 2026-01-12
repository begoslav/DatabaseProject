# E-SHOP Management System - Dokumentace

## 1. Přehled projektu

Toto je školský projekt - CLI aplikace pro správu e-shopu s MySQL databází. Aplikace implementuje **DAO pattern (D1)** pro správu dat a splňuje všechny požadavky zadání.

## 2. Implementované požadavky

### 2.1 Databázová struktura
- **5+ tabulek**: kategorie, produkty, produkt_kategorie, zakaznici, objednavky, polozky_objednavek
- **2 VIEW**: v_objednavky_s_detaily, v_skladova_dostupnost
- **M:N vazba**: produkt_kategorie
- **Všechny datové typy**:
  - Reálné číslo (DECIMAL): cena_bez_dph, sazba_dph
  - Logická hodnota (BOOLEAN): je_aktivni, poznamka
  - Výčet (ENUM): typ_produktu, stav objednávky
  - Řetězec (VARCHAR): nazev, email
  - Datum/čas (DATETIME): casova_znamka_vytvoreni, vytvoreno

### 2.2 DAO Pattern (D1)
Projekt obsahuje kompletní DAO implementaci:
- `BaseDAO` - abstraktní třída
- `KategorieDAO`, `ProduktDAO`, `ZakaznikDAO`, `ObjednavkaDAO`
- Všechny metody: find_by_id, find_all, save, delete, vlastní dotazy

### 2.3 Funkčnost

#### CRUD operace
- ✓ Produkty: seznam, detail, přidání, úprava, smazání
- ✓ Kategorie: seznam, přidání
- ✓ Zákazníci: seznam, detail, přidání
- ✓ Objednávky: seznam, detail, vytvoření, zrušení

#### Komplexní operace
- ✓ Vytvoření objednávky s více položkami (M:1 vazba) - **TRANSAKCE!**
- ✓ Zrušení objednávky se vrácením na sklad - **TRANSAKCE!**
- ✓ Automatický výpočet cen s DPH

#### Transakce
1. **Vytvoření objednávky** - atomic operace: insert objednavky + insert položek + update skladů
2. **Zrušení objednávky** - vrácení produktů na sklad + update stavu

#### Reporty (agregace ze 3+ tabulek)
1. **Report objednávek** - count, sum, min, max, avg ceny
2. **Report populárních produktů** - prodané kusy, objem, průměrná cena
3. **Report skladových stavů** - dostupnost, celková hodnota

#### Import/Export
- ✓ Import produktů z CSV
- ✓ Import produktů z JSON
- ✓ Import zákazníků z CSV
- ✓ Export produktů do CSV

### 2.4 Error Handling
- Ověření vstupů (email, PSČ, telefon, ceny)
- Databázové chyby
- Chyby konfigurací
- Výjimky s smysluplnými zprávami pro uživatele

### 2.5 Konfigurace
- `config.ini` s připojením k MySQL a aplikačním nastavením
- Možnost změny databází bez úpravy kódu

## 3. Instalace a spuštění

### Požadavky
- Python 3.7+
- MySQL 5.7+
- pip

### Krok 1: Instalace MySQL
```bash
# Windows - MySQL musí být nainstalován a spuštěn
# Obvykle na port 3306
```

### Krok 2: Vytvoření databází
```sql
mysql -u root -p < db/schema.sql
mysql -u root -p eshop < db/sample_data.sql
```

### Krok 3: Instalace Python balíčků
```bash
pip install -r requirements.txt
```

### Krok 4: Konfigurace
Upravte `config.ini`:
```ini
[database]
host = localhost
port = 3306
user = root
password = VAŠE_HESLO
database = eshop
```

### Krok 5: Spuštění
```bash
python src/main.py
```

## 4. Struktura projektu
```
DatabaseProject/
├── src/
│   ├── main.py              # Vstupní bod
│   ├── models/              # Datové modely (Product, Customer, Order...)
│   ├── database/
│   │   ├── connection.py    # Singleton pro DB připojení
│   │   └── dao/             # DAO implementace (D1 pattern)
│   ├── services/            # Business logika (objednávky, reporty, import)
│   ├── cli/                 # CLI menu a příkazy
│   └── utils/               # Validátory
├── db/
│   ├── schema.sql           # Databázové schéma
│   └── sample_data.sql      # Vzorová data
├── data/                    # CSV/JSON data pro import
├── doc/                     # Dokumentace
├── test/                    # Testovací scénáře
├── config.ini               # Konfigurace
└── requirements.txt         # Python závislosti
```

## 5. Primární klíče a indexy
- Všechny tabulky mají PRIMARY KEY
- Indexy na: email, type_produktu, stav objednávky, ID zákazníka

## 6. Relační integrita
- FOREIGN KEY s ON DELETE CASCADE/RESTRICT
- CHECK constraints (pocet > 0)
- UNIQUE constraints (nazev, email)

## 7. Problémy a řešení

| Problém | Řešení |
|---------|--------|
| Chyba připojení k DB | Zkontrolujte MySQL a config.ini |
| ImportError pro mysql | Spusťte: `pip install mysql-connector-python` |
| CSV s chybným kódováním | Ujistěte se, že je soubor v UTF-8 |
| Duplikátní email | Zákazník s tímto emailem již existuje |

## 8. Bezpečnost
- Parametrizované SQL dotazy (ochrana před SQL injection)
- Validace všech vstupů
- Šifrování hesel doporučeno pro produkci
- Transakcí zajišťují konzistenci dat

## 9. Performance
- Indexy na často vyhledávaná pole
- Efektivní SQL dotazy s JOIN operacemi
- Groupování v reportech na DB úrovni

## 10. Kontakt a podpora
Projekt byl vytvořen jako školský projekt.
