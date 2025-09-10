import sqlite3
from pathlib import Path

def criar_banco():
    """Cria o banco de dados e a tabela se não existirem"""
    db_path = Path(__file__).parent / "filmes.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS filmes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        genero TEXT NOT NULL,
        ano INTEGER NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

def adicionar_filme(titulo, genero, ano):
    """Adiciona um novo filme ao banco de dados"""
    conn = sqlite3.connect('filmes.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO filmes (titulo, genero, ano)
    VALUES (?, ?, ?)
    ''', (titulo, genero, ano))
    
    conn.commit()
    filme_id = cursor.lastrowid
    conn.close()
    
    return filme_id

def listar_filmes():
    """Retorna todos os filmes do banco de dados"""
    conn = sqlite3.connect('filmes.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, titulo, genero, ano FROM filmes ORDER BY titulo')
    filmes = cursor.fetchall()
    
    conn.close()
    return filmes

def buscar_filme_por_id(filme_id):
    """Busca um filme específico pelo ID"""
    conn = sqlite3.connect('filmes.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, titulo, genero, ano FROM filmes WHERE id = ?', (filme_id,))
    filme = cursor.fetchone()
    
    conn.close()
    return filme

def editar_filme(filme_id, titulo, genero, ano):
    """Edita um filme existente"""
    conn = sqlite3.connect('filmes.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE filmes 
    SET titulo = ?, genero = ?, ano = ?
    WHERE id = ?
    ''', (titulo, genero, ano, filme_id))
    
    conn.commit()
    conn.close()

def deletar_filme(filme_id):
    """Remove um filme do banco de dados"""
    conn = sqlite3.connect('filmes.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM filmes WHERE id = ?', (filme_id,))
    
    conn.commit()
    conn.close()