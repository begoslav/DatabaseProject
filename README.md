# E-Shop Management System - CLI

Školský projekt - CLI aplikace pro správu e-shopu s MySQL databází. 

## Designový vzor: DAO Pattern (D1)

Projekt implementuje kompletní **Data Access Object (DAO) pattern** pro separaci datové vrstvy od business logiky.

## Rychlý start

### 1. Instalace
```bash
# Instalace Python balíčků
pip install -r requirements.txt

# Vytvoření databáze
mysql -u root -p < db/schema.sql
mysql -u root -p eshop < db/sample_data.sql
```

### 2. Konfigurace
Upravte `config.ini`:
```ini
[database]
password = VAŠE_HESLO
```

### 3. Spuštění
```bash
python src/main.py
```

## Struktura projektu

```
DatabaseProject/
├── src/
│   ├── main.py                    # Vstupní bod aplikace
│   ├── models/                    # Datové modely
│   ├── database/
│   │   ├── connection.py          # DB připojení (Singleton)
│   │   └── dao/                   # DAO objekty (D1 pattern)
│   ├── services/                  # Business logika
│   ├── cli/                       # CLI menu
│   └── utils/                     # Validátory
├── db/
│   ├── schema.sql                 # Databázové schéma
│   └── sample_data.sql            # Vzorová data
├── data/                          # CSV/JSON import
├── doc/                           # Dokumentace
├── test/                          # Testovací scénáře
├── config.ini                     # Konfigurace
└── requirements.txt               # Dependencies
```

## Klíčové funkce

### Databáze
- ✓ 6 tabulek + 2 views
- ✓ M:N vazba (produkty-kategorie)
- ✓ Všechny datové typy (float, bool, enum, string, datetime)
- ✓ Indexy a relační integrita

### Aplikace
- ✓ CRUD operace na všech entitách
- ✓ **TRANSAKCE** - vytvoření/zrušení objednávek
- ✓ **3 REPORTY** - objednávky, produkty, sklady
- ✓ **IMPORT/EXPORT** - CSV, JSON
- ✓ **Validace vstupů** - email, PSČ, ceny
- ✓ **Error handling** - chybové scénáře

### DAO Pattern
```
Commands
  ├── KategorieDAO       ✓ find_by_id, find_all, save, delete
  ├── ProduktDAO         ✓ find_by_kategorie, add_kategorie, ...
  ├── ZakaznikDAO        ✓ find_by_email, find_by_mesto, ...
  └── ObjednavkaDAO      ✓ find_by_stav, add_polozka, ...
```

## Testování

3 testovací scénáře:

1. **Scénář 1** - Instalace a nastavení
2. **Scénář 2** - CRUD operace
3. **Scénář 3** - Transakce, reporty, import

Viz `/test` složka.

## Ukázkový workflow

```bash
# Spuštění
python src/main.py

# Menu:
1. Správa produktů
2. Správa kategorií  
3. Správa zákazníků
4. Správa objednávek
5. Reporty
6. Import/Export
0. Konec
```

## Transakce příklady

### Vytvoření objednávky
- Atomic operace: insert objednávky + insert položek + update skladů
- Pokud selhání: rollback všeho

### Zrušení objednávky
- Vrácení produktů na sklad
- Update stavu objednávky
- Garantovaná konzistence

## Reporty

1. **Objednávky** - COUNT, SUM, AVG, MIN, MAX ceny
2. **Populární produkty** - TOP 10 s objemem
3. **Skladové stavy** - Dostupnost a hodnota

## Ošetření chyb

| Situace | Řešení |
|---------|--------|
| Chybná konfigurace | Chybová zpráva s návodem |
| Neplatný email | Validace a odmítnutí |
| Duplicitní zákazník | Databázové omezení |
| Málo na skladě | Kontrola a upozornění |
| Chybný import | Logování chyb, pokračování |

## Technologie

- **Jazyk**: Python 3.7+
- **Databáze**: MySQL 5.7+
- **Vzor**: DAO Pattern (D1)
- **CLI**: Textuální menu s volbami

## Autor

Školský projekt

## Poznámky

- Všechny dotazy jsou parametrizované (SQL injection ochrana)
- Transakce zajišťují konzistenci dat
- DAO pattern odděluje data layer od business logiky
- Konfigurační soubor umožňuje snadnou změnu nastavení
