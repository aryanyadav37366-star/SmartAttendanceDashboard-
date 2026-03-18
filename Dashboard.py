import streamlit as st
import requests
import pandas as pd

url = "https://smartattendance-128a0-default-rtdb.asia-southeast1.firebasedatabase.app/attendance.json"

st.set_page_config(page_title="Smart Attendance", layout="wide")
st.title("📊 Smart Attendance Dashboard")

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

    st.sidebar.header("🔍 Filters")

    search = st.sidebar.text_input("Search Student")
    dates = df['Date'].unique()
    selected_date = st.sidebar.selectbox("Select Date", ["All"] + list(dates))

    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search, case=False)]

    if selected_date != "All":
        filtered_df = filtered_df[filtered_df['Date'] == selected_date]

    st.subheader("📋 Attendance Table")
    st.dataframe(filtered_df, use_container_width=True)

    st.subheader("📈 Summary")

    total_students = df['Name'].nunique()
    total_present = len(filtered_df)

    col1, col2 = st.columns(2)
    col1.metric("👨‍🎓 Total Students", total_students)
    col2.metric("✅ Present", total_present)

    st.subheader("📅 Date-wise Attendance")
    st.bar_chart(df['Date'].value_counts())

    st.subheader("❌ Absent Students")

    all_students = df['Name'].unique()

    if selected_date != "All":
        present_today = df[df['Date'] == selected_date]['Name'].unique()
        absent = [s for s in all_students if s not in present_today]

        st.write(absent if absent else "No absentees 🎉")
    else:
        st.write("Select a date")

    st.subheader("📥 Download Data")

    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='attendance.csv',
        mime='text/csv'
    )

else:
    st.warning("No data found ❌")
