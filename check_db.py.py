import sqlite3
import os

db_path = 'db.sqlite3'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Listar todas as tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("📊 TABELAS NO BANCO DE DADOS:")
    for table in tables:
        print(f" - {table[0]}")
    
    conn.close()
else:
    print("❌ Banco de dados não encontrado!")