from dadata import Dadata
import sqlite3
from tools import *


if __name__ == "__main__":
    connection = sqlite3.connect("dadata.db")
    cursor = connection.cursor()
    token = start_program(connection, cursor)
    session = Dadata(token)
    search_geo(session)
