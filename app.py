import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import altair as alt

habit_data = {
    2022: {"months": 4, "net": 44, "start_month": 9},
    2023: {"months": 12, "net": 144},
    2024: {"months": 12, "net": 158},
    2025: {"months": 8, "net": 93},
}

def calculate_stats(data):
    rows = []
    today = datetime.now()
    last_month = today - timedelta(days=30)

    first_day_this_month = datetime(last_month.year, last_month.month, 1) + timedelta(days=32)
    first_day_this_month = first_day_this_month.replace(day=1)
    last_day = first_day_this_month - timedelta(days=1)

    for year, stats in data.items():
        months = stats["months"]
        net = stats["net"]
        month_avg = round(net / months, 2) if months > 0 else 0.0

        if "start_month" in stats:
            start_of_year = datetime(year, stats["start_month"], 1)
        else:
            start_of_year = datetime(year, 1, 1)

        if year == last_month.year:
            days_elapsed = (last_day - start_of_year).days + 1
        else:
            year_end = datetime(year, 12, 31)
            days_elapsed = (year_end - start_of_year).days + 1

        avg_gap = round(days_elapsed / net, 2) if net > 0 else 0.0

        rows.append({
            "Year": year,
            "Months Logged": months,
            "Total Count": net,
            "Monthly Avg": month_avg,
            "Avg Gap (days)": avg_gap
        })

    return pd.DataFrame(rows)

df = calculate_stats(habit_data)

total_months = df["Months Logged"].sum()
total_net = df["Total Count"].sum()
overall_month_avg = round(df["Monthly Avg"].mean(), 2)
overall_gap_avg = round(df["Avg Gap (days)"].mean(), 2)

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #00BBFF 20%, #FF4400 80%);
    }
    html, body, [class*="css"]  {
        font-size: 18px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.subheader("📊 Habit Tracker Dashboard")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(
        f"""
        <div style="display:flex; gap:20px">
            <div style="background:#4776FF; padding:10px; border-radius:20px; color:black; text-align:center;">
                <h4>Total Count</h4>
                <p style="font-size:30px;">{total_net}</p>
            </div>
            <div style="background:#FFCF47; padding:10px; border-radius:20px; color:black; text-align:center;">
                <h4>Overall Monthly Avg</h4>
                <p style="font-size:30px;">{overall_month_avg:.2f}</p>
            </div>
            <div style="background:#47FF73; padding:10px; border-radius:20px; color:black; text-align:center;">
                <h4>Avg Gap (days)</h4>
                <p style="font-size:30px;">{overall_gap_avg:.2f}</p>
            </div>
            <div style="background:#FF47D2; padding:10px; border-radius:20px; color:black; text-align:center;">
                <h4>Total Months</h4>
                <p style="font-size:30px;">{total_months}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📋 Raw Data")
    st.dataframe(df)
    
    st.subheader("➕ Add New Data")
    with st.form("add_data"):
        times_done = st.number_input("Enter Last Month's Data", min_value=0)
        submit = st.form_submit_button("Add")

    if submit:
        today = datetime.now()
        last_month = today - timedelta(days=30)
        year = last_month.year
        month = last_month.month
        month_name = last_month.strftime("%B")

        if year in habit_data:
            habit_data[year]["months"] += 1
            habit_data[year]["net"] += times_done
        else:
            habit_data[year] = {"months": 1, "net": times_done, "start_month": month}

        st.success(f"✅ Added {times_done} habits for {month_name} {year}")

with col2:
    st.subheader("📈 Annual Graph")
    chart = alt.Chart(df).mark_bar().encode( 
        x=alt.X("Year:N", sort="ascending"),
        y="Total Count:Q",
        color="Year:N"
        ).properties(width=600, height=600) 
    st.altair_chart(chart, use_container_width=True)