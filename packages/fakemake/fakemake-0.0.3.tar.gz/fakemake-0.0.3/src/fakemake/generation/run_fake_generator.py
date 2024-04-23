import multiprocessing
from ..app.database import DB
from .create_persist_all import generate_data

def run_generator(sql_models_path, database_uri='sqlite:///database.db', number_of_processes=5, number_of_records=1000):
    database = DB(sql_models_path, database_uri)
    database.create_db()

    lock = multiprocessing.Lock()
    processes = []
    for _ in range(number_of_processes):
        process = multiprocessing.Process(target=generate_data, args=(lock, sql_models_path, database_uri, number_of_records//number_of_processes))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()