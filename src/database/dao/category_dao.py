"""DAO pro Kategorie"""
from src.database.dao.base_dao import BaseDAO
from src.models.category import Kategorie


class KategorieDAO(BaseDAO):
    """Data Access Object pro Kategorii"""
    
    def find_by_id(self, id_kategorie):
        """Najde kategorii podle ID"""
        query = "SELECT * FROM kategorie WHERE id_kategorie = %s"
        cursor = self._execute_query(query, (id_kategorie,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return self._row_to_entity(result)
        return None
    
    def find_all(self):
        """Vrátí všechny kategorie"""
        query = "SELECT * FROM kategorie ORDER BY nazev"
        cursor = self._execute_query(query)
        results = cursor.fetchall()
        cursor.close()
        
        return [self._row_to_entity(row) for row in results]
    
    def find_aktivni(self):
        """Vrátí všechny aktivní kategorie"""
        query = "SELECT * FROM kategorie WHERE je_aktivni = TRUE ORDER BY nazev"
        cursor = self._execute_query(query)
        results = cursor.fetchall()
        cursor.close()
        
        return [self._row_to_entity(row) for row in results]
    
    def save(self, entity):
        """Uloží nebo aktualizuje kategorii"""
        if entity.id_kategorie is None:
            return self._insert(entity)
        else:
            return self._update(entity)
    
    def _insert(self, entity):
        """Vloží novou kategorii"""
        query = """
            INSERT INTO kategorie (nazev, popis, je_aktivni)
            VALUES (%s, %s, %s)
        """
        params = (entity.nazev, entity.popis, entity.je_aktivni)
        entity.id_kategorie = self._execute_update(query, params)
        return entity
    
    def _update(self, entity):
        """Aktualizuje existující kategorii"""
        query = """
            UPDATE kategorie
            SET nazev = %s, popis = %s, je_aktivni = %s
            WHERE id_kategorie = %s
        """
        params = (entity.nazev, entity.popis, entity.je_aktivni, entity.id_kategorie)
        self._execute_update(query, params)
        return entity
    
    def delete(self, id_kategorie):
        """Smaže kategorii"""
        query = "DELETE FROM kategorie WHERE id_kategorie = %s"
        self._execute_update(query, (id_kategorie,))
    
    def _row_to_entity(self, row):
        """Konvertuje řádek z databáze na Kategorii objekt"""
        entity = Kategorie(
            id_kategorie=row['id_kategorie'],
            nazev=row['nazev'],
            popis=row['popis'],
            je_aktivni=row['je_aktivni']
        )
        return entity
