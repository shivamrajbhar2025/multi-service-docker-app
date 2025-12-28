import time
import psycopg2
import os

for i in range(10):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        break
    except psycopg2.OperationalError:
        print("Database not ready, retrying...")
        time.sleep(3)
else:
    raise Exception("Database not available")

cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
)
""")
conn.commit()
cur.close()
conn.close()
