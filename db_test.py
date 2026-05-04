import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime, timedelta
import random

def get_connection():
    return psycopg2.connect(
        host=st.secrets["db"]["host"],
        port=st.secrets["db"]["port"],
        dbname=st.secrets["db"]["dbname"],
        user=st.secrets["db"]["user"],
        password=st.secrets["db"]["password"],
        sslmode="require"
    )

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS speed_sensor (
        id SERIAL PRIMARY KEY,
        speed_kmh FLOAT,
        recorded_at TIMESTAMP
    )
""")

data = []
base_time = datetime.now()

# This part created random data
for i in range(20):
    speed_kmh = round(random.uniform(0, 140), 2)
    recorded_at = base_time - timedelta(minutes=i * 5)
    data.append((speed_kmh, recorded_at))

cursor.executemany("""
    INSERT INTO speed_sensor (speed_kmh, recorded_at)
    VALUES (%s, %s)
""", data)
conn.commit()

cursor.execute("SELECT speed_kmh, recorded_at FROM speed_sensor ORDER BY recorded_at")
rows = cursor.fetchall()
df = pd.DataFrame(rows, columns=["speed_kmh", "recorded_at"])

cursor.close()
conn.close()

st.line_chart(df.set_index("recorded_at")["speed_kmh"])