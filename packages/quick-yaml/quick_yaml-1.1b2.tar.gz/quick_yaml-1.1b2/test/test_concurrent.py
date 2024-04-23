import threading
import time
from random import randint

from src.quick_yaml.manager import QYAMLDB, QYAMLDBCoarse

# Initialize the database
db_path = "test_db.ezdb"
db = QYAMLDBCoarse(path=db_path,encrypted=False)

# Setup initial tables and data
db.create_table("test_table")
for i in range(10):
    db.insert_new_data("test_table", {"id": i, "value": f"initial_data_{i}"})


# Reader thread function
def reader_thread(db, table_name, read_count):
    for _ in range(read_count):
        entry_id = randint(0, 9)
        try:
            data = db.get_data_by_id(table_name, entry_id)
            print(f"Reader got data: {data}")
        except Exception as e:
            print(f"Reader encountered an error: {str(e)}")
        time.sleep(randint(1, 3))  # Simulate read time


# Writer thread function
def writer_thread(db, table_name, write_count):
    for _ in range(write_count):
        entry_id = randint(0, 9)

        new_value = f"updated_data_{randint(100, 200)}"
        try:

            db.update_many(table_name,{'id':{'$neq':entry_id}},{'value':new_value})
            print(f"WRITER THREAD:  No of readers {db._readers}")
            print(f"Writer updated entry {entry_id} to {new_value}")
        except Exception as e:

            print(f"Writer encountered an error: {str(e)}")
        time.sleep(randint(1, 3))  # Simulate write time


# Create thread groups
readers = []
writers = []

# Create 5 reader threads
for _ in range(10):
    t = threading.Thread(target=reader_thread, args=(db, "test_table", 5))
    readers.append(t)

# Create 2 writer threads
for _ in range(1):
    t = threading.Thread(target=writer_thread, args=(db, "test_table", 5))
    writers.append(t)

# Start all threads
for reader in readers:
    reader.start()
for writer in writers:
    writer.start()

# Wait for all threads to complete
for reader in readers:
    reader.join()
for writer in writers:
    writer.join()

print("Test complete.")
