"""Service pro generování reportů"""
from src.database.dao.order_dao import ObjednavkaDAO
from src.database.dao.product_dao import ProduktDAO
from src.database.dao.customer_dao import ZakaznikDAO
from datetime import datetime


class ReportService:
    """Service pro generování reportů"""
    
    def __init__(self):
        self.objednavka_dao = ObjednavkaDAO()
        self.produkt_dao = ProduktDAO()
        self.zakaznik_dao = ZakaznikDAO()
    
    def report_objednavky_vysledek(self):
        """Vrátí report - tržby z objednávek (agregace ze 3+ tabulek)"""
        db = self.objednavka_dao.connection
        query = """
            SELECT 
                COUNT(DISTINCT o.id_objednavky) AS pocet_objednavek,
                COUNT(DISTINCT o.id_zakaznika) AS pocet_zakazniku,
                SUM(po.pocet) AS celkem_polozek,
                MIN(o.cena_s_dph) AS min_cena,
                MAX(o.cena_s_dph) AS max_cena,
                AVG(o.cena_s_dph) AS avg_cena,
                SUM(o.cena_s_dph) AS celkove_trzby,
                o.stav
            FROM objednavky o
            LEFT JOIN polozky_objednavek po ON o.id_objednavky = po.id_objednavky
            GROUP BY o.stav
        """
        
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        
        return results
    
    def report_popularne_produkty(self, limit=10):
        """Vrátí nejpopulárnější produkty"""
        db = self.objednavka_dao.connection
        query = """
            SELECT 
                p.id_produktu,
                p.nazev,
                COUNT(po.id_polozky) AS pocet_prodani,
                SUM(po.pocet) AS celkem_kusu,
                SUM(po.pocet * po.jednotkova_cena) AS celkovy_objem_bez_dph,
                AVG(po.jednotkova_cena) AS avg_cena
            FROM produkty p
            LEFT JOIN polozky_objednavek po ON p.id_produktu = po.id_produktu
            WHERE p.je_aktivni = TRUE
            GROUP BY p.id_produktu, p.nazev
            ORDER BY celkem_kusu DESC
            LIMIT %s
        """
        
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        cursor.close()
        
        return results
    
    def report_zakaznici_vydaje(self, limit=10):
        """Vrátí zákazníky s největšími výdaji"""
        db = self.objednavka_dao.connection
        query = """
            SELECT 
                z.id_zakaznika,
                CONCAT(z.jmeno, ' ', z.prijmeni) AS jmeno,
                z.email,
                COUNT(o.id_objednavky) AS pocet_objednavek,
                SUM(o.cena_s_dph) AS celkove_vydaje,
                AVG(o.cena_s_dph) AS avg_objednavka
            FROM zakaznici z
            LEFT JOIN objednavky o ON z.id_zakaznika = o.id_zakaznika
            WHERE z.je_aktivni = TRUE
            GROUP BY z.id_zakaznika
            ORDER BY celkove_vydaje DESC
            LIMIT %s
        """
        
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        cursor.close()
        
        return results
    
    def report_skladove_stavy(self):
        """Vrátí skladový report"""
        db = self.objednavka_dao.connection
        query = """
            SELECT 
                p.id_produktu,
                p.nazev,
                p.skladem,
                p.cena_bez_dph,
                p.skladem * p.cena_bez_dph AS celkova_hodnota,
                GROUP_CONCAT(k.nazev SEPARATOR ', ') AS kategorie,
                CASE 
                    WHEN p.skladem = 0 THEN 'Vyprodáno'
                    WHEN p.skladem < 5 THEN 'Kritické'
                    WHEN p.skladem < 20 THEN 'Nízké'
                    ELSE 'Dostupné'
                END AS stav
            FROM produkty p
            LEFT JOIN produkt_kategorie pk ON p.id_produktu = pk.id_produktu
            LEFT JOIN kategorie k ON pk.id_kategorie = k.id_kategorie
            WHERE p.je_aktivni = TRUE
            GROUP BY p.id_produktu
            ORDER BY p.skladem ASC
        """
        
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        
        return results
    
    def generate_pdf_report(self, filename):
        """Generuje PDF report"""
        print(f"Report by byl vygenerován do souboru: {filename}")
        # Implementace PDF generování by zde byla s knihovnou reportlab
