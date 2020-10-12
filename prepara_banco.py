import sqlite3
print('Conectando...')
conn = sqlite3.connect("jogoteca.db")

cursor = conn.cursor()

try:
  cursor.execute('DROP TABLE jogo')
except sqlite3.OperationalError:
  pass

try:
  cursor.execute('DROP TABLE usuario')
except sqlite3.OperationalError:
  pass

criar_tabelas = '''
    CREATE TABLE `jogo` (
      `id` INTEGER PRIMARY KEY AUTOINCREMENT,
      `nome` varchar(50) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `console` varchar(20) NOT NULL
    );'''

try:
  cursor.execute(criar_tabelas)
except sqlite3.OperationalError:
  pass

criar_tabelas = '''
    CREATE TABLE `usuario` (
      `id` varchar(8) NOT NULL,
      `nome` varchar(20) NOT NULL,
      `senha` varchar(8) NOT NULL,
      PRIMARY KEY (`id`)
    );'''

try:
  cursor.execute(criar_tabelas)
except sqlite3.OperationalError:
  pass

# inserindo usuarios
cursor.executemany(
      'INSERT INTO usuario (id, nome, senha) VALUES (?, ?, ?)',
      [
            ('luan', 'Luan Marques', 'flask'),
            ('nico', 'Nico', '7a1'),
            ('danilo', 'Danilo', 'vegas')
      ])

cursor.execute('SELECT * FROM usuario')
print(' -------------  Usuários:  -------------')
for linha in cursor.fetchall():
    print(linha[1])

# inserindo jogos
cursor.executemany(
      'INSERT INTO jogo (nome, categoria, console) VALUES (?, ?, ?)',
      [
            ('God of War 4', 'Ação', 'PS4'),
            ('NBA 2k18', 'Esporte', 'Xbox One'),
            ('Rayman Legends', 'Indie', 'PS4'),
            ('Super Mario RPG', 'RPG', 'SNES'),
            ('Super Mario Kart', 'Corrida', 'SNES'),
            ('Fire Emblem Echoes', 'Estratégia', '3DS'),
      ])

cursor.execute('SELECT * FROM jogo')
print(' -------------  Jogos:  -------------')
for linha in cursor.fetchall():
    print(linha[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()
input('\nAperte ENTER para continuar...')