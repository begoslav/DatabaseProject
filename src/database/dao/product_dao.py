"""DAO pro Produkty"""
from src.database.dao.base_dao import BaseDAO
from src.models.product import Produkt


class ProduktDAO(BaseDAO):
    """Data Access Object pro Produkt"""
    
    def find_by_id(self, id_produktu):
        """Najde produkt podle ID"""
        query = "SELECT * FROM produkty WHERE id_produktu = %s"
        cursor = self._execute_query(query, (id_produktu,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return self._row_to_entity(result)
        return None
    
    def find_all(self):
        """Vrátí všechny produkty"""
        query = "SELECT * FROM produkty ORDER BY nazev"
        cursor = self._execute_query(query)
        results = cursor.fetchall()
        cursor.close()
        
        return [self._row_to_entity(row) for row in results]
    
    def find_aktivni(self):
        """Vrátí všechny aktivní produkty"""
        query = "SELECT * FROM produkty WHERE je_aktivni = TRUE ORDER BY nazev"
        cursor = self._execute_query(query)
        results = cursor.fetchall()
        cursor.close()
        
        return [self._row_to_entity(row) for row in results]
    
    def find_by_kategorie(self, id_kategorie):
        """Najde produkty v kategorii"""
        query = """
            SELECT p.* FROM produkty p
            JOIN produkt_kategorie pk ON p.id_produktu = pk.id_produktu
            WHERE pk.id_kategorie = %s AND p.je_aktivni = TRUE
            ORDER BY p.nazev
        """
        cursor = self._execute_query(query, (id_kategorie,))
        results = cursor.fetchall()
        cursor.close()
        
        return [self._row_to_entity(row) for row in results]
    
    def find_nactene(self, limit=10):
        """Vrátí produkty bez zásob"""
        query = """
            SELECT * FROM produkty
            WHERE skladem = 0 AND je_aktivni = TRUE
            ORDER BY nazev
            LIMIT %s
        """
        cursor = self._execute_query(query, (limit,))
        results = cursor.fetchall()
        cursor.close()
        
        return [self._row_to_entity(row) for row in results]
    
    def save(self, entity):
        """Uloží nebo aktualizuje produkt"""
        if entity.id_produktu is None:
            return self._insert(entity)
        else:
            return self._update(entity)
    
    def _insert(self, entity):
        """Vloží nový produkt"""
        query = """
            INSERT INTO produkty (nazev, popis, cena_bez_dph, sazba_dph, skladem, typ_produktu, je_aktivni)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            entity.nazev,
            entity.popis,
            entity.cena_bez_dph,
            entity.sazba_dph,
            entity.skladem,
            entity.typ_produktu,
            entity.je_aktivni
        )
        entity.id_produktu = self._execute_update(query, params)
        return entity
    
    def _update(self, entity):
        """Aktualizuje existující produkt"""
        query = """
            UPDATE produkty
            SET nazev = %s, popis = %s, cena_bez_dph = %s, sazba_dph = %s,
                skladem = %s, typ_produktu = %s, je_aktivni = %s
            WHERE id_produktu = %s
        """
        params = (
            entity.nazev,
            entity.popis,
            entity.cena_bez_dph,
            entity.sazba_dph,
            entity.skladem,
            entity.typ_produktu,
            entity.je_aktivni,
            entity.id_produktu
        )
        self._execute_update(query, params)
        return entity
    
    def delete(self, id_produktu):
        """Smaže produkt"""
        query = "DELETE FROM produkty WHERE id_produktu = %s"
        self._execute_update(query, (id_produktu,))
    
    def add_kategorie(self, id_produktu, id_kategorie):
        """Přidá kategorii k produktu"""
        query = """
            INSERT IGNORE INTO produkt_kategorie (id_produktu, id_kategorie)
            VALUES (%s, %s)
        """
        self._execute_update(query, (id_produktu, id_kategorie))
    
    def remove_kategorie(self, id_produktu, id_kategorie):
        """Odebere kategorii z produktu"""
        query = """
            DELETE FROM produkt_kategorie
            WHERE id_produktu = %s AND id_kategorie = %s
        """
        self._execute_update(query, (id_produktu, id_kategorie))
    
    def get_kategorie(self, id_produktu):
        """Vrátí všechny kategorie produktu"""
        query = """
            SELECT k.* FROM kategorie k
            JOIN produkt_kategorie pk ON k.id_kategorie = pk.id_kategorie
            WHERE pk.id_produktu = %s
        """
        cursor = self._execute_query(query, (id_produktu,))
        results = cursor.fetchall()
        cursor.close()
        
        return [row['id_kategorie'] for row in results]
    
    def _row_to_entity(self, row):
        """Konvertuje řádek z databáze na Produkt objekt"""
        entity = Produkt(
            id_produktu=row['id_produktu'],
            nazev=row['nazev'],
            popis=row['popis'],
            cena_bez_dph=float(row['cena_bez_dph']),
            sazba_dph=float(row['sazba_dph']),
            skladem=row['skladem'],
            typ_produktu=row['typ_produktu'],
            je_aktivni=row['je_aktivni']
        )
        return entity
