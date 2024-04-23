import importlib
from sqlalchemy import create_engine

class DB():
    def __init__(self, sql_models_path, db_uri):
        self.db_uri = db_uri
        self.sql_models_path = sql_models_path

    def create_db(self):
        models_module = importlib.import_module(self.sql_models_path)
        Base = getattr(models_module, "Base")
        engine = create_engine(self.db_uri, connect_args={'timeout': 30})
        if 'sqlite' in self.db_uri:
            Base.metadata.create_all(engine)