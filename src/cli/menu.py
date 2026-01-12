"""CLI Menu"""
from src.cli.commands import Commands
import os


class Menu:
    """Hlavní CLI menu"""
    
    def __init__(self):
        self.commands = Commands()
        self.running = True
    
    def show_main_menu(self):
        """Zobrazí hlavní menu"""
        print("\n" + "=" * 70)
        print("E-SHOP MANAGEMENT SYSTEM - CLI".center(70))
        print("=" * 70)
        print("\n1. Správa produktů")
        print("2. Správa kategorií")
        print("3. Správa zákazníků")
        print("4. Správa objednávek")
        print("5. Reporty")
        print("6. Import/Export dat")
        print("0. Konec")
        print("\n" + "-" * 70)
    
    def show_products_menu(self):
        """Submenu produktů"""
        while True:
            print("\n--- SPRÁVA PRODUKTŮ ---")
            print("1. Vypsat všechny produkty")
            print("2. Zobrazit detail produktu")
            print("3. Přidat nový produkt")
            print("4. Aktualizovat produkt")
            print("5. Smazat produkt")
            print("0. Zpět")
            
            choice = input("\nVyberte akci: ").strip()
            
            if choice == '1':
                self.commands.list_products()
            elif choice == '2':
                try:
                    pid = int(input("Zadejte ID produktu: "))
                    self.commands.view_product(pid)
                except ValueError:
                    print("✗ Neplatné ID!")
            elif choice == '3':
                try:
                    nazev = input("Název produktu: ").strip()
                    popis = input("Popis (volitelně): ").strip() or None
                    cena = input("Cena bez DPH (Kč): ").strip()
                    skladem = input("Počet kusů na skladě: ").strip()
                    sazba = input("Sazba DPH % [21]: ").strip() or "21.0"
                    typ = input("Typ (fyzicka/digitalni/sluzba) [fyzicka]: ").strip() or "fyzicka"
                    
                    self.commands.add_product(nazev, cena, skladem, popis, sazba, typ)
                except Exception as e:
                    print(f"✗ Chyba: {e}")
            elif choice == '4':
                try:
                    pid = int(input("Zadejte ID produktu: "))
                    print("Ponechte prázdné, pokud nechcete změnit...")
                    nazev = input("Nový název: ").strip() or None
                    cena = input("Nová cena: ").strip() or None
                    skladem = input("Nový počet kusů: ").strip() or None
                    
                    kwargs = {}
                    if nazev:
                        kwargs['nazev'] = nazev
                    if cena:
                        kwargs['cena_bez_dph'] = float(cena)
                    if skladem:
                        kwargs['skladem'] = int(skladem)
                    
                    self.commands.update_product(pid, **kwargs)
                except Exception as e:
                    print(f"✗ Chyba: {e}")
            elif choice == '5':
                try:
                    pid = int(input("Zadejte ID produktu k smazání: "))
                    if input("Jste si jistý? (ano/ne): ").lower() == 'ano':
                        self.commands.delete_product(pid)
                except ValueError:
                    print("✗ Neplatné ID!")
            elif choice == '0':
                break
            else:
                print("✗ Neplatná volba!")
    
    def show_categories_menu(self):
        """Submenu kategorií"""
        while True:
            print("\n--- SPRÁVA KATEGORIÍ ---")
            print("1. Vypsat všechny kategorie")
            print("2. Přidat novou kategorii")
            print("0. Zpět")
            
            choice = input("\nVyberte akci: ").strip()
            
            if choice == '1':
                self.commands.list_categories()
            elif choice == '2':
                try:
                    nazev = input("Název kategorie: ").strip()
                    popis = input("Popis (volitelně): ").strip() or None
                    self.commands.add_category(nazev, popis)
                except Exception as e:
                    print(f"✗ Chyba: {e}")
            elif choice == '0':
                break
            else:
                print("✗ Neplatná volba!")
    
    def show_customers_menu(self):
        """Submenu zákazníků"""
        while True:
            print("\n--- SPRÁVA ZÁKAZNÍKŮ ---")
            print("1. Vypsat všechny zákazníky")
            print("2. Zobrazit detail zákazníka")
            print("3. Přidat nového zákazníka")
            print("0. Zpět")
            
            choice = input("\nVyberte akci: ").strip()
            
            if choice == '1':
                self.commands.list_customers()
            elif choice == '2':
                try:
                    cid = int(input("Zadejte ID zákazníka: "))
                    self.commands.view_customer(cid)
                except ValueError:
                    print("✗ Neplatné ID!")
            elif choice == '3':
                try:
                    jmeno = input("Jméno: ").strip()
                    prijmeni = input("Příjmení: ").strip()
                    email = input("Email: ").strip()
                    telefon = input("Telefon (volitelně): ").strip() or None
                    adresa = input("Adresa: ").strip()
                    mesto = input("Město: ").strip()
                    psc = input("PSČ (formát: XXX XX): ").strip()
                    stav = input("Stav (volitelně): ").strip() or None
                    
                    self.commands.add_customer(jmeno, prijmeni, email, adresa, mesto, psc, telefon, stav)
                except Exception as e:
                    print(f"✗ Chyba: {e}")
            elif choice == '0':
                break
            else:
                print("✗ Neplatná volba!")
    
    def show_orders_menu(self):
        """Submenu objednávek"""
        while True:
            print("\n--- SPRÁVA OBJEDNÁVEK ---")
            print("1. Vypsat všechny objednávky")
            print("2. Zobrazit detail objednávky")
            print("3. Vytvořit novou objednávku")
            print("4. Zrušit objednávku")
            print("0. Zpět")
            
            choice = input("\nVyberte akci: ").strip()
            
            if choice == '1':
                self.commands.list_orders()
            elif choice == '2':
                try:
                    oid = int(input("Zadejte ID objednávky: "))
                    self.commands.view_order(oid)
                except ValueError:
                    print("✗ Neplatné ID!")
            elif choice == '3':
                try:
                    cid = int(input("ID zákazníka: "))
                    
                    polozky = []
                    while True:
                        pid = input("ID produktu (prázdné pro konec): ").strip()
                        if not pid:
                            break
                        pocet = input("Počet kusů: ").strip()
                        
                        try:
                            polozky.append({'id_produktu': int(pid), 'pocet': int(pocet)})
                            print("✓ Položka přidána")
                        except ValueError:
                            print("✗ Neplatné ID nebo počet!")
                    
                    if not polozky:
                        print("✗ Objednávka musí obsahovat alespoň jednu položku!")
                        continue
                    
                    poznamka = input("Poznámka (volitelně): ").strip() or None
                    self.commands.create_order(cid, polozky, poznamka)
                except Exception as e:
                    print(f"✗ Chyba: {e}")
            elif choice == '4':
                try:
                    oid = int(input("ID objednávky k zrušení: "))
                    if input("Jste si jistý? (ano/ne): ").lower() == 'ano':
                        self.commands.objednavka_service.zrusit_objednavku(oid)
                except Exception as e:
                    print(f"✗ Chyba: {e}")
            elif choice == '0':
                break
            else:
                print("✗ Neplatná volba!")
    
    def show_reports_menu(self):
        """Submenu reportů"""
        while True:
            print("\n--- REPORTY ---")
            print("1. Report objednávek a tržeb")
            print("2. Report nejpopulárnějších produktů")
            print("3. Report skladových stavů")
            print("0. Zpět")
            
            choice = input("\nVyberte akci: ").strip()
            
            if choice == '1':
                self.commands.show_report_objednavky()
            elif choice == '2':
                self.commands.show_report_popularne_produkty()
            elif choice == '3':
                self.commands.show_report_skladove_stavy()
            elif choice == '0':
                break
            else:
                print("✗ Neplatná volba!")
    
    def show_import_menu(self):
        """Submenu importu/exportu"""
        while True:
            print("\n--- IMPORT/EXPORT DAT ---")
            print("1. Importovat produkty (CSV)")
            print("2. Importovat produkty (JSON)")
            print("3. Importovat zákazníky (CSV)")
            print("4. Exportovat produkty (CSV)")
            print("0. Zpět")
            
            choice = input("\nVyberte akci: ").strip()
            
            if choice == '1':
                filename = input("Cesta k CSV souboru: ").strip()
                self.commands.import_produkty(filename, 'csv')
            elif choice == '2':
                filename = input("Cesta k JSON souboru: ").strip()
                self.commands.import_produkty(filename, 'json')
            elif choice == '3':
                filename = input("Cesta k CSV souboru: ").strip()
                self.commands.import_zakaznici(filename)
            elif choice == '4':
                filename = input("Cesta výstupního souboru: ").strip()
                self.commands.export_produkty(filename)
            elif choice == '0':
                break
            else:
                print("✗ Neplatná volba!")
    
    def run(self):
        """Spustí hlavní smyčku"""
        try:
            while self.running:
                self.show_main_menu()
                choice = input("Vyberte akci: ").strip()
                
                if choice == '1':
                    self.show_products_menu()
                elif choice == '2':
                    self.show_categories_menu()
                elif choice == '3':
                    self.show_customers_menu()
                elif choice == '4':
                    self.show_orders_menu()
                elif choice == '5':
                    self.show_reports_menu()
                elif choice == '6':
                    self.show_import_menu()
                elif choice == '0':
                    print("\n✓ Sbohem!")
                    self.running = False
                else:
                    print("✗ Neplatná volba!")
        
        except KeyboardInterrupt:
            print("\n\n✓ Aplikace přerušena")
        except Exception as e:
            print(f"\n✗ Chyba aplikace: {e}")
