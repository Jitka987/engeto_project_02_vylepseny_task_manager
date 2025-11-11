import pytest
import db_Vylepseny_task_manager_project_02 as db

LIBRARY="mysql"
DB_PASSW=">PASSWORD<"
HOST="localhost"
USER="root"
DATABASE="project02_testovaci"

def test_pridani_ukolu_pozitivni():
    nazev_ukolu = "Testovaci ukol"
    popis_ukolu = "Ukol slouzici k automatickemu testu PYTEST"

    conn= db.initialize_test_database(HOST, USER, DB_PASSW, DATABASE)

    cursor = conn.cursor()
    db.pridat_ukol(conn,nazev_ukolu,popis_ukolu)
    cursor.execute(f"select * from ukoly where název = '{nazev_ukolu}'")
    
    assert cursor.fetchall()[0] != None
    db.clear_database(conn,DATABASE)



def test_pridani_ukolu_negativni():
    nazev_ukolu = "Testovaci ukol spatny"
    popis_ukolu = ""

    conn= db.initialize_database(HOST, USER, DB_PASSW, DATABASE)

    cursor = conn.cursor()
    try:
        db.pridat_ukol(conn,nazev_ukolu,popis_ukolu)
    except ValueError as e:
        print(e)
    
    cursor.execute(f"select * from ukoly where název = '{nazev_ukolu}'")
    
    assert len(cursor.fetchall()) == 0
    db.clear_database(conn,DATABASE)


def test_aktualizace_ukolu_pozitivni():
    nazev_ukolu = "Testovaci ukol"
    popis_ukolu = "Ukol slouzici k automatickemu testu PYTEST"
    stav = "Hotovo"

    conn= db.initialize_test_database(HOST, USER, DB_PASSW, DATABASE)

    cursor = conn.cursor()
    db.pridat_ukol(conn,nazev_ukolu,popis_ukolu)
    cursor.execute("select ukolID from ukoly where název = %s", (nazev_ukolu,))
    ukolID = cursor.fetchone()[0]
    
    db.aktualizovat_ukol(conn, ukolID, stav)
    cursor.execute("select * from ukoly where stav = %s", (stav,))
    assert cursor.fetchall()[0] != None
    db.clear_database(conn,DATABASE)
    

def test_aktualizace_ukolu_negativní():
    nazev_ukolu = "Testovaci ukol"
    popis_ukolu = "Ukol slouzici k automatickemu testu PYTEST"
    stav = None

    conn= db.initialize_test_database(HOST, USER, DB_PASSW, DATABASE)

    cursor = conn.cursor()
    db.pridat_ukol(conn,nazev_ukolu,popis_ukolu)
    cursor.execute("select ukolID from ukoly where název = %s", (nazev_ukolu,))
    ukolID = cursor.fetchone()[0]
    try:
        db.aktualizovat_ukol(conn, ukolID, stav)
    except ValueError as e:
        print(e)
    cursor.execute("select * from ukoly where stav = %s", (stav,))
    assert len(cursor.fetchall()) == 0
    db.clear_database(conn,DATABASE)


def test_odstranit_ukol_pozitivni():
    nazev_ukolu = "Testovaci ukol"
    popis_ukolu = "Ukol slouzici k automatickemu testu PYTEST"
    
    conn= db.initialize_test_database(HOST, USER, DB_PASSW, DATABASE)

    cursor = conn.cursor()
    db.pridat_ukol(conn,nazev_ukolu,popis_ukolu)
    cursor.execute("select ukolID from ukoly where název = %s", (nazev_ukolu,))
    ukolID = cursor.fetchone()[0]
    
    db.odstranit_ukol(conn, ukolID)
    cursor.execute("select * from ukoly where ukolID = %s", (ukolID,))
    assert len(cursor.fetchall()) == 0
    db.clear_database(conn,DATABASE)


def test_odstranit_ukol_pozitivni():
    nazev_ukolu = "Testovaci ukol"
    popis_ukolu = "Ukol slouzici k automatickemu testu PYTEST"
    
    conn= db.initialize_test_database(HOST, USER, DB_PASSW, DATABASE)

    cursor = conn.cursor()
    db.pridat_ukol(conn,nazev_ukolu,popis_ukolu)
    cursor.execute("select ukolID from ukoly where název = %s", (nazev_ukolu,))
    ukoltest = cursor.fetchone()[0]
    ukolID = ukoltest + 1
    try:
        db.odstranit_ukol(conn, ukolID)
    except ValueError as e:
        print(e)
    cursor.execute("select * from ukoly where název = %s", (nazev_ukolu,))
    assert len(cursor.fetchall()) != 0
    db.clear_database(conn,DATABASE)
