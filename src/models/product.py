"""Datový model pro Produkt"""

class Produkt:
    def __init__(self, id_produktu=None, nazev=None, popis=None, cena_bez_dph=None,
                 sazba_dph=21.0, skladem=0, typ_produktu='fyzicka', je_aktivni=True):
        self.id_produktu = id_produktu
        self.nazev = nazev
        self.popis = popis
        self.cena_bez_dph = cena_bez_dph
        self.sazba_dph = sazba_dph
        self.skladem = skladem
        self.typ_produktu = typ_produktu  # 'fyzicka', 'digitalni', 'sluzba'
        self.je_aktivni = je_aktivni
        self.kategorie = []  # seznam ID kategorií

    def get_cena_s_dph(self):
        """Vrací cenu s DPH"""
        if self.cena_bez_dph is None:
            return None
        return round(self.cena_bez_dph * (1 + self.sazba_dph / 100), 2)

    def __repr__(self):
        return f"Produkt(id={self.id_produktu}, nazev='{self.nazev}', cena={self.cena_bez_dph})"
