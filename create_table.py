# Author: OpenAI Assistant, based on model Clinton Daniel, University of South Florida
# Date: 30/05/2025
# Description: This Python script assumes that you already have
# a database.db file at the root of your workspace.
# This script will CREATE all necessary tables in database.db using SQLite3.
# Execute this script before running the Flask app.
# Open a Python terminal and execute:
# python create_tables.py

import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

# TABEL: persoane
conn.execute('''
    CREATE TABLE IF NOT EXISTS persoane (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nume TEXT,
        prenume TEXT,
        sex TEXT,
        varsta INTEGER,
        tip_client TEXT,
        numar_de_telefon TEXT,
        adresa TEXT,
        oras TEXT,
        permis_conducere BOOLEAN,
        abonament_platit BOOLEAN
    )
''')

# TABEL: profil_psihologic
conn.execute('''
    CREATE TABLE IF NOT EXISTS profil_psihologic (
        id_profil INTEGER PRIMARY KEY AUTOINCREMENT,
        id_persoana INTEGER,
        predominanta_de_emisfera TEXT,
        tipologia_de_personalitate TEXT,
        intentii_viitoare TEXT,
        hobbyuri TEXT,
        preferinte_job TEXT,
        FOREIGN KEY (id_persoana) REFERENCES persoane(id)
    )
''')

# TABEL: educatie
conn.execute('''
    CREATE TABLE IF NOT EXISTS educatie (
        id_educatie INTEGER PRIMARY KEY AUTOINCREMENT,
        id_persoana INTEGER,
        nivel TEXT,
        scoala TEXT,
        FOREIGN KEY (id_persoana) REFERENCES persoane(id)
    )
''')

# TABEL: experienta_profesionala
conn.execute('''
    CREATE TABLE IF NOT EXISTS experienta_profesionala (
        id_exp INTEGER PRIMARY KEY AUTOINCREMENT,
        id_persoana INTEGER,
        loc_de_lucru_anterior TEXT,
        experienta_anterioara TEXT,
        FOREIGN KEY (id_persoana) REFERENCES persoane(id)
    )
''')

# TABEL: familie
conn.execute('''
    CREATE TABLE IF NOT EXISTS familie (
        id_familie INTEGER PRIMARY KEY AUTOINCREMENT,
        id_persoana INTEGER,
        parinti TEXT,
        FOREIGN KEY (id_persoana) REFERENCES persoane(id)
    )
''')

# TABEL: firme
conn.execute('''
    CREATE TABLE IF NOT EXISTS firme (
        id_firma INTEGER PRIMARY KEY AUTOINCREMENT,
        nume_firma TEXT,
        nr_angajati INTEGER,
        locuri_disponibile INTEGER
    )
''')


print("All tables created successfully!")
conn.execute('DROP TABLE IF EXISTS elevi')
print("Tabelul 'elevi' a fost șters cu succes.")
conn.close()
