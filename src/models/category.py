"""Datový model pro Kategorii"""

class Kategorie:
    def __init__(self, id_kategorie=None, nazev=None, popis=None, je_aktivni=True):
        self.id_kategorie = id_kategorie
        self.nazev = nazev
        self.popis = popis
        self.je_aktivni = je_aktivni

    def __repr__(self):
        return f"Kategorie(id={self.id_kategorie}, nazev='{self.nazev}')"
