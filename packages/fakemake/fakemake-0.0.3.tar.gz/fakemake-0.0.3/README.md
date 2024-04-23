# fakemake

* This is a python library to generate fake data objects and persist them into a relational database
* This uses faker, sqlalchemy, multiprocessing and other libraries
* The idea is to generate fake data objects in multiple processes to produce a large quantity of data generated
* After generating, the data will be persisted into the database defined by the user

# Arguments

There are four neccessary arguments needed to run the generator....

* sql_models_path
    * The path to your sqlalchemy models in the format of "directory.file"
    * There is no default as this is dependent on usecase
* database_uri 
    * The connection string of your database to be persisted into
    * The default is 'sqlite:///database.db'
* number_of_processes 
    * The number of processes to generate...Keep in mind the more you add the more overhead on the system
    * The default is 5
* number_of_records 
    * The number of records to be persisted
    * The default is 1000

# How to Run

```python
from fakemake import run_generator

run_generator('directory.file', 'sqlite:///database.db', 5, 1000)
```

# Additional Notes

* This framework will only pickup tables defined by CLASSES in the sqlalchemy models files...
* The more records the more time it will take to run through...
* Default values will be filled in depending on your data type...
* Ensure your columns have correct TYPES and SIZES
* Do not add too many processes...