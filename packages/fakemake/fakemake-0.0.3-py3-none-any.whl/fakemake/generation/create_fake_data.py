import random
import numpy as np
import string

def create_default_string(fake, record):
    fake_value = fake.word()
    return fake_value

def create_default_int(fake, record):
    return random.randint(1, 1000000)

def create_default_float(fake, record):
    return random.random()

def create_default_date(fake, record):
    return fake.date()

def create_email(fake, record):
    domain_names = ['yahoo', 'aol', 'gmail', 'outlook', 'iCloud', 'Mail', 'GMX', 'ProtonMail', 'example', 'test', 'company']
    domains = ['.net', '.com', '.org']
    fake_name = fake.word() + fake.first_name().lower()
    fake_number = random.randint(100, 100000)
    fake_domain = random.choice(domain_names) + random.choice(domains)
    fake_value = f"{fake_name}{fake_number}@{fake_domain}"
    return fake_value

def create_address(fake, record):
    fake_value = fake.address()
    return fake_value

def create_username(fake, record):
    fake_name = fake.last_name().lower() 
    random_string_length = random.randint(3, 10)
    fake_letters = ''.join(random.choices(string.ascii_letters, k=random_string_length))
    fake_number = random.randint(100, 100000)
    fake_value = fake_name + fake_letters + str(fake_number)
    return fake_value

def create_gender(fake, record):
    if not hasattr(record, 'gender'):
        record.gender = random.choice(['M', 'F'])
    return record.gender

def create_job(fake, record):
    fake_value = fake.job()
    return fake_value

def create_full_name(fake, record):
    if not hasattr(record, 'gender'): 
        create_gender(fake, record)
    if record.gender == 'M':
        record.first_name = fake.first_name_male()
        record.middle_name = fake.first_name_male()
        record.last_name = fake.last_name()
    else:
        record.first_name = fake.first_name_female()
        record.middle_name = fake.first_name_female()
        record.last_name = fake.last_name()
    fake_prefixes = np.random.choice(['', 'Dr. ','Prof. '], p=[0.95, 0.03, 0.02])
    fake_suffix = np.random.choice(['', ' Jr.', ' Sr.', ' III'], p=[0.91, 0.05, 0.02, 0.02])
    fake_value = random.choice([fake_prefixes + record.first_name + ' ' + record.middle_name + ' ' + record.last_name + fake_suffix])
    return fake_value

def create_first_name(fake, record):
    if not hasattr(record, 'first_name'): 
        create_full_name(fake, record)
    return record.first_name

def create_middle_name(fake, record):
    if not hasattr(record, 'middle_name'): 
        create_full_name(fake, record)
    return record.middle_name

def create_last_name(fake, record):
    if not hasattr(record, 'last_name'): 
        create_full_name(fake, record)
    return record.last_name

def create_phone(fake, record):
    return f"{random.randint(111, 999)}-{random.randint(111, 999)}-{random.randint(1111, 9999)}"

def create_ssn(fake, record):
    return f"{random.randint(111, 999)}-{random.randint(11, 99)}-{random.randint(1111, 9999)}"

def create_bank(fake, record):
    return random.choice(['Bank of America', 'Capital One', 'Morgan Stanley', 'American Express', 'JPMorgan', 'Wells Fargo', 'Chase Bank'])

def create_account_number(fake, record):
    return fake.bban()

def create_birthdate(fake, record):
    return fake.date_of_birth(minimum_age=18, maximum_age=90)

def create_country(fake, record):
    return fake.country()

def create_postal(fake, record):
    return f"{random.randint(11111, 99999)}"

def create_state(fake, record):
    return fake.state()

def create_url(fake, record):
    return fake.url()

def create_company(fake, record):
    return fake.company()

def create_text(fake, record):
    return fake.text()[:50:]

def create_sentence(fake, record):
    return fake.sentence()

def create_latitude(fake, record):
    return float(fake.latitude())

def create_longitude(fake, record):
    return float(fake.longitude())

