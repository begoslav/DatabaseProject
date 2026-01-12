"""Hlavní vstupní bod aplikace"""
import sys
import os

# Přidá projekt root do path (funguje pro oba způsoby spuštění)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.database.connection import DatabaseConnection
from src.cli.menu import Menu


def main():
    """Hlavní funkce"""
    print("\n" + "=" * 70)
    print("E-SHOP MANAGEMENT SYSTEM - Inicializace".center(70))
    print("=" * 70)
    
    try:
        # Připojí se k databázi
        db = DatabaseConnection()
        connection = db.connect('config.ini')
        
        print("\nAplikace je připravena k použití.")
        
        # Spustí CLI menu
        menu = Menu()
        menu.run()
        
        # Odpojí se od databáze
        db.disconnect()
        
    except FileNotFoundError as e:
        print(f"\n✗ Chyba: {e}")
        print("Ujistěte se, že soubor 'config.ini' existuje v kořenové složce projektu.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Kritická chyba: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
