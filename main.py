import db_Vylepseny_task_manager_project_02 as db

LIBRAR="mysql"
DB_PASSW="1111"
HOST="localhost"
USER="root"
DATABASE="project02"


if __name__ == "__main__":
    conn = db.initialize_database(HOST, USER, DB_PASSW, DATABASE)
    while True:
        try:
            #---------------    
            print("\nHlavní nabídka")
            print("1. Přidat úkol")
            print("2. Zobrazit úkoly")
            print("3. Aktualizovat úkol")
            print("4. Odstranit úkol")
            print("5. Ukončit program")

            choice = input("\nVyber možnost: ")

            if choice == "1":
                název = input("Napiš název úkolu: ")
                popis = input("Napiš popis úkolu: ")
                print("Nazev:",název," popis:",popis)
                db.pridat_ukol(conn, název, popis)

            elif choice == "2":
                ukoly = db.zobrazit_ukoly(conn)
                for ukol in ukoly:
                    print(f"ID: {ukol['ukolID']} | Název: {ukol['název']} | Popis: {ukol['popis']} | Stav: {ukol['stav']}")
               

            elif choice == "3":
                ukoly = db.zobrazit_ukoly(conn)
                for ukol in ukoly:
                    print(f"ID: {ukol['ukolID']} | Název: {ukol['název']} | Popis: {ukol['popis']} | Stav: {ukol['stav']}")
               
                ukolID = (input("\nVyberte úkol pro změnu stavu (podle ID): "))
                
                print("Pokud chcete změnit stav úkolu na 'Probíhá', vyberte možnost 1. \nPokud chcete změnit stav úkolu na 'Hotovo', vyberte možnost 2.")
                vyberstavu = (input("\nVyberte možnost změny stavu úkolu: "))
                
                if vyberstavu != "1" and vyberstavu != "2":
                    raise ValueError ("Špatný výběr stavu.")
                if vyberstavu == "1":
                    stav = "Probíhá"
                elif vyberstavu == "2":
                    stav = "Hotovo"
            
              
                db.aktualizovat_ukol(conn, ukolID, stav)
                print(f"Stav úkolu ID {ukolID} byl úspěšně změněn.")

            elif choice == "4":
                ukoly = db.zobrazit_ukoly(conn)
                for ukol in ukoly:
                    print(f"ID: {ukol['ukolID']} | Název: {ukol['název']} | Popis: {ukol['popis']} | Stav: {ukol['stav']}")
               
                ukolID = (input("\nVyberte úkol, který chcete smazat: "))
                db.odstranit_ukol(conn, ukolID)
                print(f"Úkol {ukolID} byl úspěšně smazán.")

            elif choice == "5":
                db.close_connection(conn)
                break

            else:
                print("\nNeplatná volba, zadejte číslo z nabídky.")


        except Exception as e:
            print("Něco se nepodařilo: ",e)
    

