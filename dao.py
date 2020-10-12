from models import Jogo, Usuario
import sqlite3

SQL_CRIA_JOGO = 'INSERT INTO jogo (nome, categoria, console) VALUES (?, ?, ?)'
SQL_ATUALIZA_JOGO = 'UPDATE jogo SET nome=?, categoria=?, console=? WHERE id = ?'
SQL_DELETA_JOGO = 'DELETE FROM jogo WHERE id = ?'
SQL_BUSCA_JOGOS = 'SELECT id, nome, categoria, console FROM jogo'
SQL_JOGO_POR_ID = 'SELECT id, nome, categoria, console FROM jogo WHERE id = ?'

SQL_USUARIO_POR_ID = 'SELECT id, nome, senha FROM usuario WHERE id = ?'


class JogoDao:
    def __init__(self, database):
        # não criei a conexão aqui pq o sqlite precisa usar a con. na mesma thread
        self.__database = database

    def salvar(self, jogo):
        with sqlite3.connect(self.__database) as conn:
            cursor = conn.cursor()
            if jogo.id:
                cursor.execute(SQL_ATUALIZA_JOGO, (jogo.nome, jogo.categoria, jogo.console, jogo.id))
            else:
                cursor.execute(SQL_CRIA_JOGO, (jogo.nome, jogo.categoria, jogo.console))
                jogo.id = cursor.lastrowid
            conn.commit()
        return jogo

    def listar(self):
        with sqlite3.connect(self.__database) as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_BUSCA_JOGOS)
            jogos = traduz_jogos(cursor.fetchall())
        return jogos

    def busca_por_id(self, id):
        with sqlite3.connect(self.__database) as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_JOGO_POR_ID, (id,))
            tupla = cursor.fetchone()
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        with sqlite3.connect(self.__database) as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_DELETA_JOGO, (id,))
            conn.commit()


class UsuarioDao:
    def __init__(self, database):
        self.__database = database

    def buscar_por_id(self, id):
        with sqlite3.connect(self.__database) as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_USUARIO_POR_ID, (id,))
            dados = cursor.fetchone()
            usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_jogos(jogos):
    def cria_jogo_com_tupla(tupla):
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

    return list(map(cria_jogo_com_tupla, jogos))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])
