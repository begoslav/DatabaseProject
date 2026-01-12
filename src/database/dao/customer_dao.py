"""DAO pro Zákazníky"""
from src.database.dao.base_dao import BaseDAO
from src.models.customer import Zakaznik


class ZakaznikDAO(BaseDAO):
    """Data Access Object pro Zákazníka"""
    
    def find_by_id(self, id_zakaznika):
        """Najde zákazníka podle ID"""
        query = "SELECT * FROM zakaznici WHERE id_zakaznika = %s"
        cursor = self._execute_query(query, (id_zakaznika,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return self._row_to_entity(result)
        return None
    
    def find_by_email(self, email):
        """Najde zákazníka podle emailu"""
        query = "SELECT * FROM zakaznici WHERE email = %s"
        cursor = self._execute_query(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return self._row_to_entity(result)
        return None
    
    def find_all(self):
        """Vrátí všechny zákazníky"""
        query = "SELECT * FROM zakaznici ORDER BY prijmeni, jmeno"
        cursor = self._execute_query(query)
        results = cursor.fetchall()
        cursor.close()
        
        return [self._row_to_entity(row) for row in results]
    
    def find_aktivni(self):
        """Vrátí všechny aktivní zákazníky"""
        query = "SELECT * FROM zakaznici WHERE je_aktivni = TRUE ORDER BY prijmeni, jmeno"
        cursor = self._execute_query(query)
        results = cursor.fetchall()
        cursor.close()
        
        return [self._row_to_entity(row) for row in results]
    
    def find_by_mesto(self, mesto):
        """Najde zákazníky v městě"""
        query = "SELECT * FROM zakaznici WHERE mesto = %s AND je_aktivni = TRUE ORDER BY prijmeni, jmeno"
        cursor = self._execute_query(query, (mesto,))
        results = cursor.fetchall()
        cursor.close()
        
        return [self._row_to_entity(row) for row in results]
    
    def save(self, entity):
        """Uloží nebo aktualizuje zákazníka"""
        if entity.id_zakaznika is None:
            return self._insert(entity)
        else:
            return self._update(entity)
    
    def _insert(self, entity):
        """Vloží nového zákazníka"""
        query = """
            INSERT INTO zakaznici (jmeno, prijmeni, email, telefon, adresa, mesto, psc, stav, zeme, je_aktivni)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            entity.jmeno,
            entity.prijmeni,
            entity.email,
            entity.telefon,
            entity.adresa,
            entity.mesto,
            entity.psc,
            entity.stav,
            entity.zeme,
            entity.je_aktivni
        )
        entity.id_zakaznika = self._execute_update(query, params)
        return entity
    
    def _update(self, entity):
        """Aktualizuje existujícího zákazníka"""
        query = """
            UPDATE zakaznici
            SET jmeno = %s, prijmeni = %s, email = %s, telefon = %s, adresa = %s,
                mesto = %s, psc = %s, stav = %s, zeme = %s, je_aktivni = %s, posledni_pristup = NOW()
            WHERE id_zakaznika = %s
        """
        params = (
            entity.jmeno,
            entity.prijmeni,
            entity.email,
            entity.telefon,
            entity.adresa,
            entity.mesto,
            entity.psc,
            entity.stav,
            entity.zeme,
            entity.je_aktivni,
            entity.id_zakaznika
        )
        self._execute_update(query, params)
        return entity
    
    def delete(self, id_zakaznika):
        """Smaže zákazníka"""
        query = "DELETE FROM zakaznici WHERE id_zakaznika = %s"
        self._execute_update(query, (id_zakaznika,))
    
    def count(self):
        """Vrátí počet všech zákazníků"""
        query = "SELECT COUNT(*) as count FROM zakaznici"
        cursor = self._execute_query(query)
        result = cursor.fetchone()
        cursor.close()
        return result['count'] if result else 0
    
    def _row_to_entity(self, row):
        """Konvertuje řádek z databáze na Zakaznik objekt"""
        entity = Zakaznik(
            id_zakaznika=row['id_zakaznika'],
            jmeno=row['jmeno'],
            prijmeni=row['prijmeni'],
            email=row['email'],
            telefon=row['telefon'],
            adresa=row['adresa'],
            mesto=row['mesto'],
            psc=row['psc'],
            stav=row['stav'],
            zeme=row['zeme'],
            je_aktivni=row['je_aktivni']
        )
        entity.registrovan = row['registrovan']
        entity.posledni_pristup = row['posledni_pristup']
        return entity
