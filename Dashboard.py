import streamlit as st
import requests
import pandas as pd

# Firebase URL
url = "https://smartattendance-128a0-default-rtdb.asia-southeast1.firebasedatabase.app/attendance.json"

st.title("📊 Smart Attendance Dashboard")

# Fetch data
res = requests.get(url)
data = res.json()

records = []

if data:
    for date in data:
        for name in data[date]:
            time = data[date][name]['time']
            type_ = data[date][name]['type']

            records.append({
                "Name": name,
                "Date": date,
                "Time": time,
                "Type": type_
            })

df = pd.DataFrame(records)

if not df.empty:
    st.subheader("📋 Attendance Table")
    st.dataframe(df)

    st.subheader("📈 Summary")

    total_students = df['Name'].nunique()
    total_entries = len(df)

    st.write(f"👨‍🎓 Total Students: {total_students}")
    st.write(f"✅ Total Attendance: {total_entries}")

    st.subheader("📅 Date-wise Attendance")
    st.bar_chart(df['Date'].value_counts())
else:
    st.write("No data found ❌")