"""CLI příkazy"""
from src.database.dao.category_dao import KategorieDAO
from src.database.dao.product_dao import ProduktDAO
from src.database.dao.customer_dao import ZakaznikDAO
from src.database.dao.order_dao import ObjednavkaDAO
from src.services.order_service import ObjednavkaService
from src.services.report_service import ReportService
from src.services.import_service import ImportService
from src.models.product import Produkt
from src.models.category import Kategorie
from src.models.customer import Zakaznik
from src.utils.validators import Validators


class Commands:
    """CLI příkazy"""
    
    def __init__(self):
        self.kategorie_dao = KategorieDAO()
        self.produkt_dao = ProduktDAO()
        self.zakaznik_dao = ZakaznikDAO()
        self.objednavka_dao = ObjednavkaDAO()
        self.objednavka_service = ObjednavkaService()
        self.report_service = ReportService()
        self.import_service = ImportService()
    
    # ========== PRODUKTY ==========
    
    def add_product(self, nazev, cena_bez_dph, skladem, popis=None, sazba_dph=21.0, typ='fyzicka'):
        """Přidá nový produkt"""
        try:
            if not Validators.validate_price(cena_bez_dph):
                raise ValueError("Cena musí být kladné číslo!")
            if not Validators.validate_positive_int(skladem):
                raise ValueError("Počet kusů musí být kladné číslo!")
            if not Validators.validate_enum(typ, ['fyzicka', 'digitalni', 'sluzba']):
                raise ValueError("Neplatný typ produktu!")
            
            produkt = Produkt(
                nazev=nazev,
                popis=popis,
                cena_bez_dph=float(cena_bez_dph),
                sazba_dph=float(sazba_dph),
                skladem=int(skladem),
                typ_produktu=typ
            )
            self.produkt_dao.save(produkt)
            print(f"✓ Produkt '{nazev}' byl přidán (ID: {produkt.id_produktu})")
            return produkt
        except Exception as e:
            print(f"✗ Chyba: {e}")
            return None
    
    def list_products(self):
        """Vypíše všechny produkty"""
        try:
            produkty = self.produkt_dao.find_aktivni()
            if not produkty:
                print("Žádné produkty v databázi")
                return
            
            print(f"\n{'ID':>4} {'Název':<30} {'Cena':<10} {'Skladem':<8} {'Typ':<10}")
            print("-" * 70)
            
            for p in produkty:
                print(f"{p.id_produktu:>4} {p.nazev:<30} {p.cena_bez_dph:>9.2f} {p.skladem:>7} {p.typ_produktu:<10}")
            
            print(f"\nCelkem: {len(produkty)} produktů")
        except Exception as e:
            print(f"✗ Chyba: {e}")
    
    def view_product(self, id_produktu):
        """Zobrazí detaily produktu"""
        try:
            produkt = self.produkt_dao.find_by_id(id_produktu)
            if not produkt:
                print(f"Produkt ID {id_produktu} neexistuje!")
                return
            
            print(f"\n=== Produkt: {produkt.nazev} ===")
            print(f"ID: {produkt.id_produktu}")
            print(f"Popis: {produkt.popis or '-'}")
            print(f"Cena bez DPH: {produkt.cena_bez_dph:.2f} Kč")
            print(f"DPH (sazba): {produkt.sazba_dph:.2f}%")
            print(f"Cena s DPH: {produkt.get_cena_s_dph():.2f} Kč")
            print(f"Na skladě: {produkt.skladem} ks")
            print(f"Typ: {produkt.typ_produktu}")
            print(f"Aktivní: {'Ano' if produkt.je_aktivni else 'Ne'}")
            
            # Kategorie
            kategorie = self.produkt_dao.get_kategorie(id_produktu)
            if kategorie:
                kat_names = [self.kategorie_dao.find_by_id(k).nazev for k in kategorie]
                print(f"Kategorie: {', '.join(kat_names)}")
        except Exception as e:
            print(f"✗ Chyba: {e}")
    
    def update_product(self, id_produktu, **kwargs):
        """Aktualizuje produkt"""
        try:
            produkt = self.produkt_dao.find_by_id(id_produktu)
            if not produkt:
                print(f"Produkt ID {id_produktu} neexistuje!")
                return
            
            for key, value in kwargs.items():
                if value is not None:
                    if key == 'cena_bez_dph' and not Validators.validate_price(value):
                        raise ValueError("Cena musí být kladné číslo!")
                    if key == 'skladem' and not Validators.validate_positive_int(value):
                        raise ValueError("Počet kusů musí být kladné číslo!")
                    setattr(produkt, key, value)
            
            self.produkt_dao.save(produkt)
            print(f"✓ Produkt '{produkt.nazev}' byl aktualizován")
            return produkt
        except Exception as e:
            print(f"✗ Chyba: {e}")
            return None
    
    def delete_product(self, id_produktu):
        """Smaže produkt"""
        try:
            produkt = self.produkt_dao.find_by_id(id_produktu)
            if not produkt:
                print(f"Produkt ID {id_produktu} neexistuje!")
                return
            
            self.produkt_dao.delete(id_produktu)
            print(f"✓ Produkt '{produkt.nazev}' byl smazán")
        except Exception as e:
            print(f"✗ Chyba: {e}")
    
    # ========== KATEGORIE ==========
    
    def add_category(self, nazev, popis=None):
        """Přidá novou kategorii"""
        try:
            kategorie = Kategorie(nazev=nazev, popis=popis)
            self.kategorie_dao.save(kategorie)
            print(f"✓ Kategorie '{nazev}' byla přidána (ID: {kategorie.id_kategorie})")
            return kategorie
        except Exception as e:
            print(f"✗ Chyba: {e}")
            return None
    
    def list_categories(self):
        """Vypíše všechny kategorie"""
        try:
            kategorie = self.kategorie_dao.find_aktivni()
            if not kategorie:
                print("Žádné kategorie v databázi")
                return
            
            print(f"\n{'ID':>4} {'Název':<30} {'Popis':<30}")
            print("-" * 70)
            
            for k in kategorie:
                popis = k.popis[:27] + "..." if k.popis and len(k.popis) > 30 else k.popis or "-"
                print(f"{k.id_kategorie:>4} {k.nazev:<30} {popis:<30}")
            
            print(f"\nCelkem: {len(kategorie)} kategorií")
        except Exception as e:
            print(f"✗ Chyba: {e}")
    
    # ========== ZÁKAZNÍCI ==========
    
    def add_customer(self, jmeno, prijmeni, email, adresa, mesto, psc, telefon=None, stav=None):
        """Přidá nového zákazníka"""
        try:
            if not Validators.validate_email(email):
                raise ValueError("Neplatný formát emailu!")
            if not Validators.validate_postal_code(psc):
                raise ValueError("Neplatný formát PSČ (měl by být XXX XX)!")
            if telefon and not Validators.validate_phone(telefon):
                raise ValueError("Neplatný formát telefonního čísla!")
            
            zakaznik = Zakaznik(
                jmeno=jmeno,
                prijmeni=prijmeni,
                email=email,
                telefon=telefon,
                adresa=adresa,
                mesto=mesto,
                psc=psc,
                stav=stav
            )
            self.zakaznik_dao.save(zakaznik)
            print(f"✓ Zákazník '{jmeno} {prijmeni}' byl přidán (ID: {zakaznik.id_zakaznika})")
            return zakaznik
        except Exception as e:
            print(f"✗ Chyba: {e}")
            return None
    
    def list_customers(self):
        """Vypíše všechny zákazníky"""
        try:
            zakaznici = self.zakaznik_dao.find_aktivni()
            if not zakaznici:
                print("Žádní zákazníci v databázi")
                return
            
            print(f"\n{'ID':>4} {'Jméno':<20} {'Email':<30} {'Město':<15}")
            print("-" * 70)
            
            for z in zakaznici:
                print(f"{z.id_zakaznika:>4} {z.get_full_name():<20} {z.email:<30} {z.mesto:<15}")
            
            print(f"\nCelkem: {len(zakaznici)} zákazníků")
        except Exception as e:
            print(f"✗ Chyba: {e}")
    
    def view_customer(self, id_zakaznika):
        """Zobrazí detaily zákazníka"""
        try:
            zakaznik = self.zakaznik_dao.find_by_id(id_zakaznika)
            if not zakaznik:
                print(f"Zákazník ID {id_zakaznika} neexistuje!")
                return
            
            print(f"\n=== Zákazník: {zakaznik.get_full_name()} ===")
            print(f"ID: {zakaznik.id_zakaznika}")
            print(f"Email: {zakaznik.email}")
            print(f"Telefon: {zakaznik.telefon or '-'}")
            print(f"Adresa: {zakaznik.adresa}")
            print(f"Město: {zakaznik.mesto}, {zakaznik.psc}")
            print(f"Stát: {zakaznik.stav or '-'}, {zakaznik.zeme}")
            print(f"Registrován: {zakaznik.registrovan}")
            print(f"Poslední přístup: {zakaznik.posledni_pristup or '-'}")
            print(f"Aktivní: {'Ano' if zakaznik.je_aktivni else 'Ne'}")
        except Exception as e:
            print(f"✗ Chyba: {e}")
    
    # ========== OBJEDNÁVKY ==========
    
    def create_order(self, id_zakaznika, polozky, poznamka=None):
        """Vytvoří novou objednávku"""
        try:
            objednavka = self.objednavka_service.vytvorit_objednavku(id_zakaznika, polozky, poznamka)
            print(f"✓ Objednávka #{objednavka.id_objednavky} byla vytvořena")
            print(f"  Cena bez DPH: {objednavka.cena_bez_dph:.2f} Kč")
            print(f"  Cena s DPH: {objednavka.cena_s_dph:.2f} Kč")
            return objednavka
        except Exception as e:
            print(f"✗ Chyba: {e}")
            return None
    
    def list_orders(self):
        """Vypíše všechny objednávky"""
        try:
            objednavky = self.objednavka_service.list_objednavky()
            if not objednavky:
                print("Žádné objednávky v databázi")
                return
            
            print(f"\n{'ID':>4} {'Zákazník':<25} {'Položek':<8} {'Cena s DPH':<12} {'Stav':<12}")
            print("-" * 70)
            
            for o in objednavky:
                zakaznik = self.zakaznik_dao.find_by_id(o.id_zakaznika)
                zakaznik_jmeno = zakaznik.get_full_name() if zakaznik else "?"
                print(f"{o.id_objednavky:>4} {zakaznik_jmeno:<25} {len(o.polozky):<8} {o.cena_s_dph:>11.2f} {o.stav:<12}")
            
            print(f"\nCelkem: {len(objednavky)} objednávek")
        except Exception as e:
            print(f"✗ Chyba: {e}")
    
    def view_order(self, id_objednavky):
        """Zobrazí detaily objednávky"""
        try:
            objednavka = self.objednavka_service.get_objednavka(id_objednavky)
            if not objednavka:
                print(f"Objednávka ID {id_objednavky} neexistuje!")
                return
            
            zakaznik = self.zakaznik_dao.find_by_id(objednavka.id_zakaznika)
            
            print(f"\n=== Objednávka #{objednavka.id_objednavky} ===")
            print(f"Zákazník: {zakaznik.get_full_name() if zakaznik else '?'}")
            print(f"Vytvořena: {objednavka.casova_znamka_vytvoreni}")
            print(f"Stav: {objednavka.stav}")
            
            print(f"\nPoložky:")
            print(f"{'ID':>4} {'Produkt':<30} {'Ks':<5} {'Jedn.cena':<12} {'Cena':<12}")
            print("-" * 65)
            
            for p in objednavka.polozky:
                produkt = self.produkt_dao.find_by_id(p.id_produktu)
                produkt_jmeno = produkt.nazev if produkt else "?"
                cena = p.get_cena_se_slevou()
                print(f"{p.id_polozky:>4} {produkt_jmeno:<30} {p.pocet:<5} {p.jednotkova_cena:>11.2f} {cena:>11.2f}")
            
            print("-" * 65)
            print(f"Cena bez DPH: {objednavka.cena_bez_dph:.2f} Kč")
            print(f"DPH ({objednavka.sazba_dph}%): {(objednavka.cena_s_dph - objednavka.cena_bez_dph):.2f} Kč")
            print(f"Cena s DPH: {objednavka.cena_s_dph:.2f} Kč")
        except Exception as e:
            print(f"✗ Chyba: {e}")
    
    # ========== REPORTY ==========
    
    def show_report_objednavky(self):
        """Zobrazí report objednávek"""
        try:
            results = self.report_service.report_objednavky_vysledek()
            
            print(f"\n{'=== REPORT: OBJEDNÁVKY ===' :<50}")
            print("-" * 70)
            
            for row in results:
                print(f"\nStav: {row['stav']}")
                print(f"  Počet objednávek: {row['pocet_objednavek']}")
                print(f"  Počet zákazníků: {row['pocet_zakazniku']}")
                print(f"  Celkem položek: {row['celkem_polozek'] or 0}")
                print(f"  Min cena: {row['min_cena']:.2f if row['min_cena'] else '-'} Kč")
                print(f"  Max cena: {row['max_cena']:.2f if row['max_cena'] else '-'} Kč")
                print(f"  Průměr cena: {row['avg_cena']:.2f if row['avg_cena'] else '-'} Kč")
                print(f"  Celkové tržby: {row['celkove_trzby']:.2f if row['celkove_trzby'] else '-'} Kč")
        except Exception as e:
            print(f"✗ Chyba: {e}")
    
    def show_report_popularne_produkty(self):
        """Zobrazí report populárních produktů"""
        try:
            results = self.report_service.report_popularne_produkty(limit=10)
            
            print(f"\n{'=== REPORT: NEJPOPULÁRNĚJŠÍ PRODUKTY ===' :<50}")
            print("-" * 90)
            print(f"{'Název':<30} {'Prodáno ks':<12} {'Objem (Kč)':<15} {'Avg cena':<12}")
            print("-" * 90)
            
            for row in results:
                print(f"{row['nazev']:<30} {row['celkem_kusu'] or 0:<12} {row['celkovy_objem_bez_dph'] or 0:.2f} {row['avg_cena'] or 0:.2f}")
        except Exception as e:
            print(f"✗ Chyba: {e}")
    
    def show_report_skladove_stavy(self):
        """Zobrazí report skladových stavů"""
        try:
            results = self.report_service.report_skladove_stavy()
            
            print(f"\n{'=== REPORT: SKLADOVÉ STAVY ===' :<50}")
            print("-" * 100)
            print(f"{'Produkt':<25} {'Skladem':<10} {'Cena':<12} {'Hodnota (Kč)':<15} {'Stav':<15}")
            print("-" * 100)
            
            for row in results:
                print(f"{row['nazev']:<25} {row['skladem']:<10} {row['cena_bez_dph']:<12.2f} {row['celkova_hodnota'] or 0:<15.2f} {row['stav']:<15}")
        except Exception as e:
            print(f"✗ Chyba: {e}")
    
    # ========== IMPORT/EXPORT ==========
    
    def import_produkty(self, filename, format='csv'):
        """Importuje produkty"""
        try:
            if format.lower() == 'csv':
                imported, errors = self.import_service.import_produkty_csv(filename)
            elif format.lower() == 'json':
                imported, errors = self.import_service.import_produkty_json(filename)
            else:
                print(f"Nepodporovaný formát: {format}")
                return
            
            if errors:
                print(f"⚠ Bylo {len(errors)} chyb při importu")
        except Exception as e:
            print(f"✗ Chyba: {e}")
    
    def import_zakaznici(self, filename):
        """Importuje zákazníky"""
        try:
            imported, errors = self.import_service.import_zakaznici_csv(filename)
            if errors:
                print(f"⚠ Bylo {len(errors)} chyb při importu")
        except Exception as e:
            print(f"✗ Chyba: {e}")
    
    def export_produkty(self, filename):
        """Exportuje produkty"""
        try:
            self.import_service.export_produkty_csv(filename)
        except Exception as e:
            print(f"✗ Chyba: {e}")
