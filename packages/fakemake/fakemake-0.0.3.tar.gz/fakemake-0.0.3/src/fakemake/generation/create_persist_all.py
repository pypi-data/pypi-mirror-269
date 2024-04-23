import importlib
import random
from sqlalchemy import create_engine, Integer, String, DateTime, func, Date, Float
from sqlalchemy.orm import sessionmaker
import faker
from datetime import datetime, date
from .create_fake_data import *
from ..utils.record_keeper import Record
import warnings

warnings.filterwarnings('ignore')

string_column_handlers = {
    'occupation': create_job,
    'username': create_username,
    'first_name': create_first_name,
    'middle_name': create_middle_name,
    'last_name': create_last_name,
    'gender': create_gender,
    'address': create_address,
    'postal': create_postal,
    'acc_num': create_account_number,
    'phone': create_phone,
    'country': create_country,
    'bank': create_bank,
    'email': create_email,
    'name': create_full_name,
    'ssn': create_ssn,
    'job': create_job,
    'url': create_url,
    'company': create_company,
    'business': create_company,
    'text': create_text,
    'description': create_text,
    'bio': create_text,
    'summary': create_text,
    'sentence': create_sentence,
    'body': create_sentence,
    'title': create_sentence,
}

int_column_handlers = {
    'account': create_account_number,
    'acc': create_account_number,
    'routing': create_account_number,
    'rout': create_account_number,
    'bank': create_account_number,
}

float_column_handlers = {
    'longitude': create_longitude,
    'latitude': create_latitude
}

date_column_handlers = {
    'birth': create_birthdate
}

def generate_data(lock, sql_models_path, database_uri, number_of_records):
    models_module = importlib.import_module(sql_models_path)
    engine = create_engine(database_uri, connect_args={'timeout': 30})
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    
    fake = faker.Faker(random.randint(1, 1000))

    local_string_handlers = string_column_handlers
    local_int_handlers = int_column_handlers
    local_float_handlers = float_column_handlers
    local_date_handlers = date_column_handlers

    sampled_foreign_key_values = {}
    
    for _ in range(number_of_records):
        record = Record()
        for attr_name in dir(models_module):
            model_class = getattr(models_module, attr_name)
            if hasattr(model_class, '__table__'):
                model_instance = model_class()
                for column in model_class.__table__.columns:
                    if column.primary_key:
                        continue
                    elif column.foreign_keys:
                        referenced_column = list(column.foreign_keys)[0].column
                        referenced_table_name = referenced_column.table.name
                        
                        if referenced_table_name in sampled_foreign_key_values:
                            referenced_values = sampled_foreign_key_values[referenced_table_name]
                        else:
                            referenced_values = session.query(referenced_column).order_by(func.random()).limit(100).all()
                            sampled_foreign_key_values[referenced_table_name] = referenced_values
                        if referenced_values:
                            fake_fk_value = random.choice(referenced_values)[0]
                        else:
                            fake_fk_value = random.randint(1, number_of_records)
                        setattr(model_instance, column.name, fake_fk_value)
                    else:
                        if isinstance(column.type, Integer):
                            for key, handler in local_int_handlers.items():
                                if key in column.name.lower():
                                    fake_int_value = handler(fake, record)
                                    break
                            else:
                                fake_int_value = create_default_int(fake, record)
                            setattr(model_instance, column.name, fake_int_value)
                        elif isinstance(column.type, String):
                            for key, handler in local_string_handlers.items():
                                if key in column.name.lower():
                                    fake_str_value = handler(fake, record)
                                    break
                            else:
                                fake_str_value = create_default_string(fake, record)
                            setattr(model_instance, column.name, fake_str_value)
                        elif isinstance(column.type, Float):
                            for key, handler in local_float_handlers.items():
                                if key in column.name.lower():
                                    fake_float_value = handler(fake, record)
                                    break
                            else:
                                fake_float_value = create_default_float(fake, record)
                            setattr(model_instance, column.name, fake_float_value)
                        elif isinstance(column.type, Date):
                            for key, handler in local_date_handlers.items():
                                if key in column.name.lower():
                                    fake_date_value = handler(fake, record)
                                    break
                            else:
                                fake_date_value = create_default_date(fake, record)
                            setattr(model_instance, column.name, fake_date_value)
                        elif isinstance(column.type, DateTime):
                            fake_dt_value = datetime.now()
                            setattr(model_instance, column.name, fake_dt_value)
                with lock:
                    session.add(model_instance)
    with lock:
        try:
            session.commit()
            session.close()
        except Exception as e:
            print(e)
            print('NOTE: Bypassing error...Continuing the generation...')
