"""DAO pro Objednávky"""
from src.database.dao.base_dao import BaseDAO
from src.models.order import Objednavka, PolozkaObjednavky


class ObjednavkaDAO(BaseDAO):
    """Data Access Object pro Objednávku"""
    
    def find_by_id(self, id_objednavky):
        """Najde objednávku podle ID"""
        query = "SELECT * FROM objednavky WHERE id_objednavky = %s"
        cursor = self._execute_query(query, (id_objednavky,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            entity = self._row_to_entity(result)
            entity.polozky = self._get_polozky(id_objednavky)
            return entity
        return None
    
    def find_all(self):
        """Vrátí všechny objednávky"""
        query = "SELECT * FROM objednavky ORDER BY casova_znamka_vytvoreni DESC"
        cursor = self._execute_query(query)
        results = cursor.fetchall()
        cursor.close()
        
        entities = []
        for row in results:
            entity = self._row_to_entity(row)
            entity.polozky = self._get_polozky(row['id_objednavky'])
            entities.append(entity)
        return entities
    
    def find_by_zakaznik(self, id_zakaznika):
        """Najde objednávky zákazníka"""
        query = "SELECT * FROM objednavky WHERE id_zakaznika = %s ORDER BY casova_znamka_vytvoreni DESC"
        cursor = self._execute_query(query, (id_zakaznika,))
        results = cursor.fetchall()
        cursor.close()
        
        entities = []
        for row in results:
            entity = self._row_to_entity(row)
            entity.polozky = self._get_polozky(row['id_objednavky'])
            entities.append(entity)
        return entities
    
    def find_by_stav(self, stav):
        """Najde objednávky se stavem"""
        query = "SELECT * FROM objednavky WHERE stav = %s ORDER BY casova_znamka_vytvoreni DESC"
        cursor = self._execute_query(query, (stav,))
        results = cursor.fetchall()
        cursor.close()
        
        entities = []
        for row in results:
            entity = self._row_to_entity(row)
            entity.polozky = self._get_polozky(row['id_objednavky'])
            entities.append(entity)
        return entities
    
    def save(self, entity):
        """Uloží nebo aktualizuje objednávku"""
        if entity.id_objednavky is None:
            return self._insert(entity)
        else:
            return self._update(entity)
    
    def _insert(self, entity):
        """Vloží novou objednávku"""
        query = """
            INSERT INTO objednavky (id_zakaznika, stav, poznamka, cena_bez_dph, sazba_dph, cena_s_dph)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            entity.id_zakaznika,
            entity.stav,
            entity.poznamka,
            entity.cena_bez_dph,
            entity.sazba_dph,
            entity.cena_s_dph
        )
        entity.id_objednavky = self._execute_update(query, params)
        return entity
    
    def _update(self, entity):
        """Aktualizuje existující objednávku"""
        query = """
            UPDATE objednavky
            SET id_zakaznika = %s, stav = %s, poznamka = %s, cena_bez_dph = %s, sazba_dph = %s, cena_s_dph = %s
            WHERE id_objednavky = %s
        """
        params = (
            entity.id_zakaznika,
            entity.stav,
            entity.poznamka,
            entity.cena_bez_dph,
            entity.sazba_dph,
            entity.cena_s_dph,
            entity.id_objednavky
        )
        self._execute_update(query, params)
        return entity
    
    def delete(self, id_objednavky):
        """Smaže objednávku"""
        query = "DELETE FROM objednavky WHERE id_objednavky = %s"
        self._execute_update(query, (id_objednavky,))
    
    def _get_polozky(self, id_objednavky):
        """Vrátí všechny položky objednávky"""
        query = "SELECT * FROM polozky_objednavek WHERE id_objednavky = %s"
        cursor = self._execute_query(query, (id_objednavky,))
        results = cursor.fetchall()
        cursor.close()
        
        polozky = []
        for row in results:
            polozka = PolozkaObjednavky(
                id_polozky=row['id_polozky'],
                id_objednavky=row['id_objednavky'],
                id_produktu=row['id_produktu'],
                pocet=row['pocet'],
                jednotkova_cena=float(row['jednotkova_cena']),
                sleva_procenta=float(row['sleva_procenta'])
            )
            polozky.append(polozka)
        return polozky
    
    def add_polozka(self, id_objednavky, id_produktu, pocet, jednotkova_cena, sleva_procenta=0):
        """Přidá položku do objednávky"""
        query = """
            INSERT INTO polozky_objednavek (id_objednavky, id_produktu, pocet, jednotkova_cena, sleva_procenta)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (id_objednavky, id_produktu, pocet, jednotkova_cena, sleva_procenta)
        return self._execute_update(query, params)
    
    def remove_polozka(self, id_polozky):
        """Odebere položku z objednávky"""
        query = "DELETE FROM polozky_objednavek WHERE id_polozky = %s"
        self._execute_update(query, (id_polozky,))
    
    def update_polozka(self, id_polozky, pocet, sleva_procenta=0):
        """Aktualizuje položku objednávky"""
        query = """
            UPDATE polozky_objednavek
            SET pocet = %s, sleva_procenta = %s
            WHERE id_polozky = %s
        """
        params = (pocet, sleva_procenta, id_polozky)
        self._execute_update(query, params)
    
    def _row_to_entity(self, row):
        """Konvertuje řádek z databáze na Objednavka objekt"""
        entity = Objednavka(
            id_objednavky=row['id_objednavky'],
            id_zakaznika=row['id_zakaznika'],
            stav=row['stav']
        )
        entity.casova_znamka_vytvoreni = row['casova_znamka_vytvoreni']
        entity.casova_znamka_posledni_zmena = row['casova_znamka_posledni_zmena']
        entity.poznamka = row['poznamka']
        entity.cena_bez_dph = float(row['cena_bez_dph'])
        entity.sazba_dph = float(row['sazba_dph'])
        entity.cena_s_dph = float(row['cena_s_dph'])
        return entity
