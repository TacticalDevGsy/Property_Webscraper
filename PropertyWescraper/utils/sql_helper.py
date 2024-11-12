from sqlalchemy import create_engine, text
from config import SqlDetails

class MysqlConnector:

    def __init__(self):
        self.sql_engine = create_engine(SqlDetails.db_driver, echo=True)

def build_db_tables_for_install():
    engine = MysqlConnector()
    with engine.sql_engine.connect() as connection:
        connection.execute(text("CREATE TABLE new_properties (unique_id1 VARCHAR(20), "
                                "unique_id2 int, "
                                "title VARCHAR(30), "
                                "price VARCHAR(30),"
                                "parish VARCHAR(20),"
                                "bedrooms int, "
                                "bathrooms int, "
                                "dateAdded DATE)"))

if __name__ == "__main__":
    build_db_tables_for_install()
