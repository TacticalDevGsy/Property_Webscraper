from sqlalchemy import create_engine, text
from config import SqlDetails

class MysqlConnector:

    def __init__(self):
        self.sql_engine = create_engine(SqlDetails.db_driver, echo=True)

def build_db_tables_for_install():
    engine = MysqlConnector()
    with engine.sql_engine.connect() as connection:
        connection.execute(text("CREATE TABLE example (id INTEGER, name VARCHAR(20))"))
