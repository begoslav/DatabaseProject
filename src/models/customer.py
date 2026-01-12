"""Datový model pro Zákazníka"""
from datetime import datetime

class Zakaznik:
    def __init__(self, id_zakaznika=None, jmeno=None, prijmeni=None, email=None,
                 telefon=None, adresa=None, mesto=None, psc=None, stav=None,
                 zeme='Česká republika', je_aktivni=True):
        self.id_zakaznika = id_zakaznika
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.email = email
        self.telefon = telefon
        self.adresa = adresa
        self.mesto = mesto
        self.psc = psc
        self.stav = stav
        self.zeme = zeme
        self.je_aktivni = je_aktivni
        self.registrovan = None
        self.posledni_pristup = None

    def get_full_name(self):
        """Vrací celé jméno"""
        return f"{self.jmeno} {self.prijmeni}"

    def __repr__(self):
        return f"Zakaznik(id={self.id_zakaznika}, jmeno='{self.jmeno}', email='{self.email}')"
