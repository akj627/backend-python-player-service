import os
import sqlite3
from sqlalchemy import create_engine

class PlayerService:
    def __init__(self, conn= None):
        if conn is None:
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'player.db')
            conn = sqlite3.connect(db_path)
        self.conn = conn
        self.cursor = conn.cursor()
        self.columns = self.__get_columns()

    def get_all_players(self):

        query = "SELECT * FROM players"
        result = self.cursor.execute(query).fetchall()
        players = []
        for row in result:
            dic = self.__convert_row_to_dict(row)
            players.append(dic)

        return players
    
    def search_by_player(self, player_id):

        query = "SELECT * FROM players WHERE playerId='{}'".format(player_id)
        result = self.cursor.execute(query).fetchall()

        dic = {}

        for row in result:
            dic = self.__convert_row_to_dict(row)
        return dic

    def search_by_country(self, birth_country):

        query = "SELECT * FROM players WHERE birthCountry='{}'".format(birth_country)
        result = self.cursor.execute(query).fetchall()

        return result


    def __convert_row_to_dict(self, row):
        dic = { self.columns[i]: row[i] for i in range(len(row)) }
        return dic


    def __get_columns(self):
        self.cursor.execute("PRAGMA table_info(players)")
        columns = [column[1] for column in self.cursor.fetchall()]
        return columns