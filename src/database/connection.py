"""Připojení k MySQL databázi"""
import mysql.connector
from mysql.connector import Error
import configparser
import os


class DatabaseConnection:
    """Singleton třída pro správu databázového připojení"""
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def connect(self, config_file='config.ini'):
        """Připojí se k databázi"""
        if self._connection and self._connection.is_connected():
            return self._connection

        try:
            config = configparser.ConfigParser()
            if not os.path.exists(config_file):
                raise FileNotFoundError(f"Konfigurační soubor '{config_file}' nebyl nalezen!")
            
            config.read(config_file)
            
            if not config.has_section('database'):
                raise ValueError("Konfigurační soubor neobsahuje sekci 'database'!")
            
            self._connection = mysql.connector.connect(
                host=config.get('database', 'host'),
                port=config.getint('database', 'port'),
                user=config.get('database', 'user'),
                password=config.get('database', 'password'),
                database=config.get('database', 'database'),
                charset=config.get('database', 'charset', fallback='utf8mb4')
            )
            
            print("✓ Připojení k databázi navázáno")
            return self._connection
        
        except Error as e:
            print(f"✗ Chyba připojení k databázi: {e}")
            raise
        except (FileNotFoundError, ValueError, configparser.Error) as e:
            print(f"✗ Chyba konfigurace: {e}")
            raise

    def disconnect(self):
        """Odpojí se od databáze"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("✓ Připojení k databázi uzavřeno")

    def get_connection(self):
        """Vrací aktuální připojení"""
        if not self._connection or not self._connection.is_connected():
            self.connect()
        return self._connection

    def execute_query(self, query, params=None):
        """Provede dotaz a vrací výsledky"""
        try:
            cursor = self._connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except Error as e:
            print(f"✗ Chyba při spuštění dotazu: {e}")
            raise

    def commit(self):
        """Potvrdí transakci"""
        try:
            self._connection.commit()
        except Error as e:
            print(f"✗ Chyba při potvrzování transakce: {e}")
            raise

    def rollback(self):
        """Vrátí transakci"""
        try:
            self._connection.rollback()
        except Error as e:
            print(f"✗ Chyba při vracení transakce: {e}")
            raise
