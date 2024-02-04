import sqlite3

def create_db():
    con = sqlite3.connect(database=r'hms.db')
    cur = con.cursor()

    # admin table
    cur.execute('CREATE TABLE IF NOT EXISTS "admin" ( "id"	INTEGER NOT NULL UNIQUE, "username"	TEXT NOT NULL, "email"	TEXT NOT NULL, "gender"	TEXT NOT NULL, "phone"	TEXT NOT NULL, "address"	TEXT NOT NULL, "password"	TEXT NOT NULL, PRIMARY KEY("id" AUTOINCREMENT) )')
    con.commit()

    # employee table
    cur.execute('CREATE TABLE IF NOT EXISTS "employee" ("id" INTEGER NOT NULL UNIQUE,"username"	text,"email" text,"gender" text,"phone"	text,"address" text,"salary" text,PRIMARY KEY("id" AUTOINCREMENT))')
    con.commit()

    # customer table
    cur.execute('CREATE TABLE IF NOT EXISTS "customer" ( "id"	INTEGER NOT NULL UNIQUE, "name"	TEXT NOT NULL, "email"	TEXT NOT NULL, "phone"	TEXT NOT NULL UNIQUE, "gender"	TEXT NOT NULL, "nationality"	TEXT NOT NULL, "idtype"	TEXT NOT NULL, "idnumber"	TEXT NOT NULL, "address"	TEXT NOT NULL, PRIMARY KEY("id" AUTOINCREMENT) )')
    con.commit()

    # reservation table
    cur.execute('CREATE TABLE IF NOT EXISTS "reservation" ( "id" INTEGER NOT NULL UNIQUE, "contact"	TEXT NOT NULL, "checkin" TEXT NOT NULL, "checkout"	TEXT NOT NULL, "roomtype"	TEXT NOT NULL, "roomno"	TEXT NOT NULL, PRIMARY KEY("id" AUTOINCREMENT) )')
    con.commit()

    # room table
    cur.execute('CREATE TABLE IF NOT EXISTS "room" ( "id" INTEGER NOT NULL UNIQUE, "floor"	TEXT NOT NULL, "roomno"	TEXT NOT NULL, "roomtype"	TEXT NOT NULL, PRIMARY KEY("id" AUTOINCREMENT) )')
    con.commit()

    # event table
    cur.execute('CREATE TABLE IF NOT EXISTS "event" ( "id"	INTEGER NOT NULL UNIQUE, "title"	TEXT NOT NULL, "details"	TEXT NOT NULL, "date"	TEXT NOT NULL, "time"	TEXT NOT NULL, PRIMARY KEY("id" AUTOINCREMENT) )')
    con.commit()



create_db()