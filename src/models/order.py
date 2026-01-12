"""Datový model pro Objednávku"""
from datetime import datetime

class PolozkaObjednavky:
    def __init__(self, id_polozky=None, id_objednavky=None, id_produktu=None,
                 pocet=1, jednotkova_cena=None, sleva_procenta=0):
        self.id_polozky = id_polozky
        self.id_objednavky = id_objednavky
        self.id_produktu = id_produktu
        self.pocet = pocet
        self.jednotkova_cena = jednotkova_cena
        self.sleva_procenta = sleva_procenta

    def get_cena_bez_slevy(self):
        """Vrací cenu bez slevy"""
        if self.jednotkova_cena is None:
            return None
        return round(self.pocet * self.jednotkova_cena, 2)

    def get_cena_se_slevou(self):
        """Vrací cenu se slevou"""
        cena = self.get_cena_bez_slevy()
        if cena is None:
            return None
        sleva = cena * self.sleva_procenta / 100
        return round(cena - sleva, 2)


class Objednavka:
    def __init__(self, id_objednavky=None, id_zakaznika=None, stav='nova'):
        self.id_objednavky = id_objednavky
        self.id_zakaznika = id_zakaznika
        self.casova_znamka_vytvoreni = None
        self.casova_znamka_posledni_zmena = None
        self.stav = stav  # 'nova', 'potvrzena', 'zaplacena', 'vyrazena', 'dorucena', 'zrusena'
        self.poznamka = None
        self.cena_bez_dph = 0
        self.sazba_dph = 21.0
        self.cena_s_dph = 0
        self.polozky = []  # seznam PolozkaObjednavky

    def add_polozka(self, polozka):
        """Přidá položku do objednávky"""
        self.polozky.append(polozka)

    def remove_polozka(self, id_polozky):
        """Odebere položku z objednávky"""
        self.polozky = [p for p in self.polozky if p.id_polozky != id_polozky]

    def __repr__(self):
        return f"Objednavka(id={self.id_objednavky}, zakaznik_id={self.id_zakaznika}, stav='{self.stav}')"
