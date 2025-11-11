import mysql.connector
from mysql.connector import Error
from datetime import date

#db_name = "project02"

def connect_to_db(host, user, password, database):
    try:
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    except Error as e:
        raise ConnectionError(f"Database connection failed: {e}")

# --- Databázové funkce ---
def initialize_database(host, user, password, db_name):
    try :
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        connection.database = db_name

        cursor.execute("""CREATE TABLE IF NOT EXISTS ukoly
                (
                ukolID int primary key AUTO_INCREMENT,
                název varchar(255) not null,
                popis varchar(255) not null,
                stav varchar(255) default 'Nezahajeno',
                datum_vytvoření datetime default CURRENT_TIMESTAMP
                );
            """)
        connection.commit()
        return connection
    except Error as e:
        raise RuntimeError(f"Chyba pri inicializaci databaze: {e}")
    
    
def initialize_test_database(host, user, password, db_name):
    try :
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        connection.database = db_name

        cursor.execute("""CREATE TABLE IF NOT EXISTS ukoly
                (
                ukolID int primary key AUTO_INCREMENT,
                název varchar(255) not null,
                popis varchar(255) not null,
                stav varchar(255) default 'Nezahajeno',
                datum_vytvoření datetime default CURRENT_TIMESTAMP
                );
            """)
        connection.commit()
        return connection
    except Error as e:
        raise RuntimeError(f"Chyba pri inicializaci databaze: {e}")
    
def clear_database(conn, db_name):
    cursor = conn.cursor()
    cursor.execute(f"DROP database {db_name}")
    conn.commit()
    cursor.close()


def pridat_ukol(connection, název, popis):
    if not connection:
        raise RuntimeError("No database connection.")
    if not název:
        raise ValueError("Název není vyplněný.")
    if not popis:
        raise ValueError("Popis není vyplněný.")

    cursor = connection.cursor()

    cursor.execute(
        "insert into ukoly(název, popis) values(%s, %s)", (název, popis))
    connection.commit()

def zobrazit_ukoly(connection):
    if not connection:
        raise RuntimeError("No database connection.")
    cursor = connection.cursor()
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from ukoly where not stav ='Hotovo'")
    ukoly = cursor.fetchall()   
    if not ukoly:
        raise ValueError("\nV seznamu nejsou žádné úkoly.")
    return ukoly

def aktualizovat_ukol(connection, ukolID, stav):
    if not connection:
        raise RuntimeError("No database connection.")

    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from ukoly where ukolID = %s", (ukolID,))
    ukol = cursor.fetchone()

    if not ukol:
        raise ValueError("Špatné číslo úkolu.")
            
    if stav is None:
        raise ValueError("Neplatny stav, musi byt 'Probiha' nebo 'Hotovo'.")
    
    cursor.execute("update ukoly set stav=%s where ukolID=%s",(stav, ukolID))
    connection.commit()


def odstranit_ukol(connection, ukolID):
    if not connection:
        raise RuntimeError("No database connection.")

    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from ukoly where ukolID = %s", (ukolID,))
    ukol = cursor.fetchone()

    if not ukol:
        raise ValueError("Špatné číslo úkolu, zkuste to znovu.")

    cursor.execute("delete from ukoly where ukolID = %s", (ukolID,))
    connection.commit()


def close_connection(connection):
    if connection:
        connection.close()



def main():
    try:
        conn = connect_to_db()
    except ValueError as e:
        print(f"Nelze navázat spojení s databází: {e}")
        return
    # Uzivatelske menu
    while True:
        print("\nHlavní nabídka")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")

        choice = input("\nVyber možnost: ")

        if choice == "1":
            pridat_ukol(conn)
        elif choice == "2":
            zobrazit_ukoly(conn)
        elif choice == "3":
            aktualizovat_ukol(conn)
        elif choice == "4":
            odstranit_ukol(conn)
        elif choice == "5":
            print("\nProgram bude ukončen.")
            break
        else:
            print("\nNeplatná volba, zadejte číslo z nabídky.")

    conn.close()

if __name__ == "__main__":
    main()
