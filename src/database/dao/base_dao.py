"""Základní DAO třída"""
from abc import ABC, abstractmethod
from src.database.connection import DatabaseConnection


class BaseDAO(ABC):
    """Abstraktní základní třída pro všechny DAO"""
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.connection = self.db.get_connection()
    
    @abstractmethod
    def find_by_id(self, id):
        """Najde entitu podle ID"""
        pass
    
    @abstractmethod
    def find_all(self):
        """Vrátí všechny entity"""
        pass
    
    @abstractmethod
    def save(self, entity):
        """Uloží nebo aktualizuje entitu"""
        pass
    
    @abstractmethod
    def delete(self, id):
        """Smaže entitu"""
        pass
    
    def _execute_query(self, query, params=None):
        """Provede dotaz"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except Exception as e:
            raise Exception(f"Chyba databáze: {e}")
    
    def _execute_update(self, query, params=None):
        """Provede update/insert/delete a potvrdí"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Chyba databáze: {e}")
