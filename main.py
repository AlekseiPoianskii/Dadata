from dadata import Dadata
import sqlite3
from tools import *


if __name__ == "__main__":
    connection = sqlite3.connect("dadata.db")
    cursor = connection.cursor()
    user = start_program(connection, cursor)
    session = Dadata(user[1])
    search_geo(session, user)
    print(END_MESSAGE)
