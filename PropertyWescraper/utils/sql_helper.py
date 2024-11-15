from sqlalchemy import (create_engine,
                        text, Column, Integer,
                        Sequence, String, Date,
                        Float, BIGINT, MetaData,
                        Table, INT, select, insert, update)
from config import SqlDetails
from sqlalchemy.engine import result

class MysqlConnector:

    def __init__(self, table_name=None):
        self.sql_engine = create_engine(SqlDetails.db_driver)
        self.table_name = table_name

    def select_data(self):
        meta_data = MetaData()
        meta_data.reflect(bind=self.sql_engine)
        new_properties = meta_data.tables[self.table_name]
        query = select(new_properties)
        for col in query.columns:
            print(col)

        with self.sql_engine.connect() as conn:
            for row in conn.execute(query):
                print(row)

    def insert_data(self):
        meta_data = MetaData()
        meta_data.reflect(bind=self.sql_engine)
        new_properties = meta_data.tables[self.table_name]
        stmt = insert(new_properties).values(id="12345", title="Testing")

        with self.sql_engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()

def build_db_tables_for_install():

    engine = MysqlConnector()
    meta_data = MetaData()

    Table("new_properties",meta_data,
                           Column("unique_id1", Integer, primary_key=True),
                           Column("unique_id2", Integer),
                           Column("title", String(30)),
                           Column("price", String(30)),
                           Column("parish", String(20)),
                           Column("bedrooms", Integer),
                           Column("bathrooms", Integer),
                           Column("dateAdded", Date)
    )

    meta_data.create_all(engine.sql_engine.connect())

if __name__ == "__main__":
    test = MysqlConnector()
    test.insert_data()
