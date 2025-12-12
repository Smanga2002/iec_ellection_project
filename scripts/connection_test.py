import os
import urllib.parse
from sqlalchemy import create_engine, text

#Get connection details from environment variables
USER = os.environ.get("POSTGRES_USER")
RAW_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
PASSWORD = urllib.parse.quote_plus(RAW_PASSWORD)  # ENCODE SPECIAL CHARACTERS
HOST = os.environ.get("POSTGRES_HOST")
DB = os.environ.get("POSTGRES_DB")
PORT = os.environ.get("POSTGRES_PORT")

def test_db_connection():
    try:
        # Construct the connection URL
        db_url = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
        engine = create_engine(db_url)

        # Test connection by executing a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as is_connected"))
            print("Database Connection Successful!")
            print(f"Query Result: {result.fetchone()}")
            print(f"Container IP of DB: {engine.url.host}") # Shows connection through 'db'

        # Validation 3: Check if source files are recognized (Placeholder in /data)
        data_path = "/Users/SmangalisoOageneg/Projects/iec_ellection_project/data/2025_Local_Election.csv"
        if os.path.exists(data_path):
            print(f"Source file placeholder found at: {data_path}")
        else:
            print(f"Source file placeholder NOT found at: {data_path}")

    except Exception as e:
        print(f"Database Connection Failed: {e}")

if __name__ == "__main__":
    test_db_connection()