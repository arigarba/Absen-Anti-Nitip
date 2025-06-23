import streamlit as st
import pandas as pd
import os
import time 
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Waktu
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp = datetime.fromtimestamp(ts).strftime("%H:%M")

# Auto-refresh
count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

if count == 0:
    st.write("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Count: {count}")


base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "attendance", "Absen_" + date + ".csv")

# Baca CSV
if os.path.exists(base_dir):
    df = pd.read_csv(csv_path)
    st.dataframe(df.style.highlight_max(axis=0))
else:
    st.warning(f"File {base_dir} tidak ditemukan. Belum ada data absen hari ini.")
