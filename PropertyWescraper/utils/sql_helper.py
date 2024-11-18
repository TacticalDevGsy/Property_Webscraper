from sqlalchemy import (create_engine,
                        text, Column, Integer,
                        Sequence, String, Date,
                        Float, BIGINT, MetaData,
                        Table, INT, select, insert, update)
from config import SqlDetails
from sqlalchemy.engine import result

# from tests.testfiles import new_listings


class MysqlConnector:

    def __init__(self, table_name=None):
        self.sql_engine = create_engine(SqlDetails.db_driver)
        self.table_name = table_name

    def select_data(self, values: list):
        meta_data = MetaData()
        meta_data.reflect(bind=self.sql_engine)
        new_properties = meta_data.tables[self.table_name]
        query = select(new_properties.c.unique_id1).where(new_properties.c.unique_id1.in_(values))
        #for col in query.columns:
        #    print(col)

        with self.sql_engine.connect() as conn:
            return [value[0] for value in conn.execute(query).fetchall()]

    def insert_data(self, *args):
        meta_data = MetaData()
        meta_data.reflect(bind=self.sql_engine)
        insert_to_table = meta_data.tables[self.table_name]
        query_stmt_add = insert(insert_to_table).values(*args)

        with self.sql_engine.connect() as conn:
            conn.execute(query_stmt_add)
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
    test = MysqlConnector("new_properties")
    test.select_data()
