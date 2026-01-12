import csv
import json
import xml.etree.ElementTree as ET
from src.database.dao.product_dao import ProduktDAO
from src.database.dao.category_dao import KategorieDAO
from src.database.dao.customer_dao import ZakaznikDAO
from src.models.product import Produkt
from src.models.category import Kategorie
from src.models.customer import Zakaznik


class ImportService:
    """Service pro import dat"""
    
    def __init__(self):
        self.produkt_dao = ProduktDAO()
        self.kategorie_dao = KategorieDAO()
        self.zakaznik_dao = ZakaznikDAO()
    
    def import_produkty_csv(self, filename):
        """Importuje produkty z CSV souboru"""
        imported = 0
        errors = []
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=',')
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        produkt = Produkt(
                            nazev=row['nazev'],
                            popis=row.get('popis', ''),
                            cena_bez_dph=float(row['cena_bez_dph']),
                            sazba_dph=float(row.get('sazba_dph', 21.0)),
                            skladem=int(row['skladem']),
                            typ_produktu=row.get('typ_produktu', 'fyzicka'),
                            je_aktivni=row.get('je_aktivni', 'true').lower() == 'true'
                        )
                        self.produkt_dao.save(produkt)
                        imported += 1
                    except Exception as e:
                        errors.append(f"Řádek {row_num}: {e}")
            
            print(f"✓ Importováno {imported} produktů z {filename}")
            if errors:
                print("⚠ Chyby při importu:")
                for error in errors[:5]:
                    print(f"  - {error}")
            
            return imported, errors
        
        except FileNotFoundError:
            raise Exception(f"Soubor '{filename}' nebyl nalezen!")
        except Exception as e:
            raise Exception(f"Chyba při importu: {e}")
    
    def import_zakaznici_csv(self, filename):
        """Importuje zákazníky z CSV souboru"""
        imported = 0
        errors = []
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=',')
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        zakaznik = Zakaznik(
                            jmeno=row['jmeno'],
                            prijmeni=row['prijmeni'],
                            email=row['email'],
                            telefon=row.get('telefon', ''),
                            adresa=row['adresa'],
                            mesto=row['mesto'],
                            psc=row['psc'],
                            stav=row.get('stav', ''),
                            zeme=row.get('zeme', 'Česká republika'),
                            je_aktivni=row.get('je_aktivni', 'true').lower() == 'true'
                        )
                        self.zakaznik_dao.save(zakaznik)
                        imported += 1
                    except Exception as e:
                        errors.append(f"Řádek {row_num}: {e}")
            
            print(f"✓ Importováno {imported} zákazníků z {filename}")
            if errors:
                print("⚠ Chyby při importu:")
                for error in errors[:5]:
                    print(f"  - {error}")
            
            return imported, errors
        
        except FileNotFoundError:
            raise Exception(f"Soubor '{filename}' nebyl nalezen!")
        except Exception as e:
            raise Exception(f"Chyba při importu: {e}")
    
    def import_produkty_json(self, filename):
        """Importuje produkty z JSON souboru"""
        imported = 0
        errors = []
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if not isinstance(data, list):
                    data = [data]
                
                for row_num, item in enumerate(data, start=1):
                    try:
                        produkt = Produkt(
                            nazev=item['nazev'],
                            popis=item.get('popis', ''),
                            cena_bez_dph=float(item['cena_bez_dph']),
                            sazba_dph=float(item.get('sazba_dph', 21.0)),
                            skladem=int(item['skladem']),
                            typ_produktu=item.get('typ_produktu', 'fyzicka'),
                            je_aktivni=item.get('je_aktivni', True)
                        )
                        self.produkt_dao.save(produkt)
                        imported += 1
                    except Exception as e:
                        errors.append(f"Položka {row_num}: {e}")
            
            print(f"✓ Importováno {imported} produktů z {filename}")
            if errors:
                print("⚠ Chyby při importu:")
                for error in errors[:5]:
                    print(f"  - {error}")
            
            return imported, errors
        
        except FileNotFoundError:
            raise Exception(f"Soubor '{filename}' nebyl nalezen!")
        except json.JSONDecodeError as e:
            raise Exception(f"Chyba v JSON formátu: {e}")
        except Exception as e:
            raise Exception(f"Chyba při importu: {e}")
    
    def export_produkty_csv(self, filename):
        """Exportuje produkty do CSV souboru"""
        try:
            produkty = self.produkt_dao.find_all()
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow(['id_produktu', 'nazev', 'popis', 'cena_bez_dph', 'sazba_dph', 'skladem', 'typ_produktu', 'je_aktivni'])
                
                for produkt in produkty:
                    writer.writerow([
                        produkt.id_produktu,
                        produkt.nazev,
                        produkt.popis,
                        produkt.cena_bez_dph,
                        produkt.sazba_dph,
                        produkt.skladem,
                        produkt.typ_produktu,
                        '1' if produkt.je_aktivni else '0'
                    ])
            
            print(f"✓ Exportováno {len(produkty)} produktů do {filename}")
            return len(produkty)
        
        except Exception as e:
            raise Exception(f"Chyba při exportu: {e}")
