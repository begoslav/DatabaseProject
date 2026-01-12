"""Service pro správu objednávek - obsahuje transakce"""
from src.database.dao.order_dao import ObjednavkaDAO
from src.database.dao.product_dao import ProduktDAO
from src.database.dao.customer_dao import ZakaznikDAO
from src.models.order import Objednavka, PolozkaObjednavky
from datetime import datetime


class ObjednavkaService:
    """Service pro objednávky - obsahuje business logiku"""
    
    def __init__(self):
        self.objednavka_dao = ObjednavkaDAO()
        self.produkt_dao = ProduktDAO()
        self.zakaznik_dao = ZakaznikDAO()
    
    def vytvorit_objednavku(self, id_zakaznika, polozky_data, poznamka=None):
        """
        Vytvoří novou objednávku s položkami - TRANSAKCE!
        polozky_data = [{'id_produktu': X, 'pocet': Y}, ...]
        Vrací vytvořenou objednávku nebo vyvolá výjimku
        """
        try:
            # Ověření zákazníka
            zakaznik = self.zakaznik_dao.find_by_id(id_zakaznika)
            if not zakaznik:
                raise ValueError(f"Zákazník ID {id_zakaznika} neexistuje!")
            
            # Tvorba objednávky
            objednavka = Objednavka(id_zakaznika=id_zakaznika, stav='nova')
            objednavka.poznamka = poznamka
            
            # Vypočet cen
            cena_bez_dph = 0
            sazba_dph = 21.0
            
            # Zpracování položek a ověření zásob
            for polozka_info in polozky_data:
                id_produktu = polozka_info['id_produktu']
                pocet = polozka_info['pocet']
                
                produkt = self.produkt_dao.find_by_id(id_produktu)
                if not produkt:
                    raise ValueError(f"Produkt ID {id_produktu} neexistuje!")
                
                # Ověření dostupnosti
                if produkt.skladem < pocet:
                    raise ValueError(f"Produkt '{produkt.nazev}' není dostupný v požadovaném množství! "
                                   f"Na skladě: {produkt.skladem}, požadováno: {pocet}")
                
                # Vytvoření položky
                polozka = PolozkaObjednavky(
                    id_produktu=id_produktu,
                    pocet=pocet,
                    jednotkova_cena=produkt.cena_bez_dph
                )
                objednavka.add_polozka(polozka)
                
                cena_bez_dph += polozka.get_cena_se_slevou()
            
            # Výpočet konečné ceny
            objednavka.cena_bez_dph = round(cena_bez_dph, 2)
            objednavka.sazba_dph = sazba_dph
            objednavka.cena_s_dph = round(cena_bez_dph * (1 + sazba_dph / 100), 2)
            
            # TRANSAKCE - vložení objednávky
            db = self.objednavka_dao.connection
            try:
                # Uloží objednávku
                objednavka = self.objednavka_dao.save(objednavka)
                
                # Vloží položky a aktualizuje zásoby
                for polozka in objednavka.polozky:
                    self.objednavka_dao.add_polozka(
                        objednavka.id_objednavky,
                        polozka.id_produktu,
                        polozka.pocet,
                        polozka.jednotkova_cena,
                        polozka.sleva_procenta
                    )
                    
                    # Aktualizace skladových zásob
                    produkt = self.produkt_dao.find_by_id(polozka.id_produktu)
                    produkt.skladem -= polozka.pocet
                    self.produkt_dao.save(produkt)
                
                # Potvrzení transakce
                db.commit()
                print(f"✓ Objednávka #{objednavka.id_objednavky} byla vytvořena")
                return objednavka
                
            except Exception as e:
                db.rollback()
                raise Exception(f"Chyba při vytváření objednávky: {e}")
        
        except Exception as e:
            raise Exception(f"Chyba: {e}")
    
    def zrusit_objednavku(self, id_objednavky):
        """Zruší objednávku a vrátí produkty na sklad - TRANSAKCE!"""
        try:
            objednavka = self.objednavka_dao.find_by_id(id_objednavky)
            if not objednavka:
                raise ValueError(f"Objednávka ID {id_objednavky} neexistuje!")
            
            if objednavka.stav == 'zrusena':
                raise ValueError("Objednávka je již zrušena!")
            
            db = self.objednavka_dao.connection
            try:
                # Vrácení produktů na sklad
                for polozka in objednavka.polozky:
                    produkt = self.produkt_dao.find_by_id(polozka.id_produktu)
                    produkt.skladem += polozka.pocet
                    self.produkt_dao.save(produkt)
                
                # Aktualizace stavu objednávky
                objednavka.stav = 'zrusena'
                self.objednavka_dao.save(objednavka)
                
                # Potvrzení transakce
                db.commit()
                print(f"✓ Objednávka #{id_objednavky} byla zrušena")
                return objednavka
                
            except Exception as e:
                db.rollback()
                raise Exception(f"Chyba při rušení objednávky: {e}")
        
        except Exception as e:
            raise Exception(f"Chyba: {e}")
    
    def aktualizovat_stav(self, id_objednavky, novy_stav):
        """Aktualizuje stav objednávky"""
        validni_stavy = ['nova', 'potvrzena', 'zaplacena', 'vyrazena', 'dorucena', 'zrusena']
        if novy_stav not in validni_stavy:
            raise ValueError(f"Neplatný stav: {novy_stav}")
        
        objednavka = self.objednavka_dao.find_by_id(id_objednavky)
        if not objednavka:
            raise ValueError(f"Objednávka ID {id_objednavky} neexistuje!")
        
        objednavka.stav = novy_stav
        self.objednavka_dao.save(objednavka)
        print(f"✓ Stav objednávky #{id_objednavky} byl změněn na '{novy_stav}'")
        return objednavka
    
    def get_objednavka(self, id_objednavky):
        """Vrátí objednávku s detaily"""
        return self.objednavka_dao.find_by_id(id_objednavky)
    
    def list_objednavky(self):
        """Vrátí všechny objednávky"""
        return self.objednavka_dao.find_all()
    
    def list_objednavky_zakaznika(self, id_zakaznika):
        """Vrátí objednávky konkrétního zákazníka"""
        return self.objednavka_dao.find_by_zakaznik(id_zakaznika)
