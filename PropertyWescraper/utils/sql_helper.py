from sqlalchemy import create_engine, text, Column, Integer, Sequence, String, Date, Float, BIGINT, MetaData, Table
from sqlalchemy.orm import sessionmaker
from config import SqlDetails

class MysqlConnector:

    def __init__(self):
        self.sql_engine = create_engine(SqlDetails.db_driver, echo=True)

def build_db_tables_for_install():

    meta_data = MetaData()

    new_properties = Table(
                    "user_account",
                    meta_data,
                    Column("id", Integer, primary_key=True),
                    Column("name", String(30)),
                    Column("fullname", String),)

    #engine = MysqlConnector()
    #with engine.sql_engine.connect() as connection:
    #    connection.execute(text("CREATE TABLE new_properties (unique_id1 VARCHAR(20), "
    #                            "unique_id2 int, "
    #                            "title VARCHAR(30), "
    #                            "price VARCHAR(30),"
    #                            "parish VARCHAR(20),"
    #                            "bedrooms int, "
    #                            "bathrooms int, "
    #                            "dateAdded DATE)"))

if __name__ == "__main__":
    build_db_tables_for_install()
