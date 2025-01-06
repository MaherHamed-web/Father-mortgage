import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from dateutil.relativedelta import relativedelta  # To handle month-by-month increments

# Set the initial mortgage details
remaining_balance = 168000  # Initial remaining mortgage in Riyals
monthly_payment = 1667      # Monthly payment in Riyals
start_date = datetime(2025, 1, 1)  # Assume payments start January 2025

# Calculate the total months and end date
total_months = remaining_balance // monthly_payment
end_date = start_date + relativedelta(months=+total_months)

# Toggle for Language
language = st.radio("Select Language / اختر اللغة", ("English", "العربية"))

# Language-specific texts
if language == "English":
    st.title("Mortgage Payment Tracker")
    st.subheader("Mortgage Details")
    current_date = datetime.now()
    elapsed_months = ((current_date.year - start_date.year) * 12) + (current_date.month - start_date.month)
    current_balance = remaining_balance - (elapsed_months * monthly_payment)

    if current_balance < 0:
        current_balance = 0

    st.write(f"### Current Month: {current_date.strftime('%B %Y')}")
    st.write(f"### Remaining Balance: {current_balance:.2f} Riyals")
    st.write(f"### Expected End Date: {end_date.strftime('%B %Y')}")

    # Generate the repayment table
    st.subheader("Upcoming Payment Schedule")
    table_data = []
    next_balance = current_balance
    next_month = current_date.replace(day=1) if current_balance > 0 else end_date

    for i in range(1, total_months + 1):  # Show until the mortgage is paid off
        next_balance -= monthly_payment
        if next_balance < 0:
            next_balance = 0
        table_data.append({
            "Month": next_month.strftime('%B %Y'),
            "Year": next_month.year,  # Add year for yearly grouping
            "Monthly Payment (Riyals)": monthly_payment,
            "Remaining Balance (Riyals)": round(next_balance, 2)
        })
        next_month += relativedelta(months=+1)
        if next_balance <= 0:
            break

    df = pd.DataFrame(table_data)
    st.table(df)

elif language == "العربية":
    st.title("متابعة سداد الرهن العقاري")
    st.subheader("تفاصيل الرهن العقاري")
    current_date = datetime.now()
    elapsed_months = ((current_date.year - start_date.year) * 12) + (current_date.month - start_date.month)
    current_balance = remaining_balance - (elapsed_months * monthly_payment)

    if current_balance < 0:
        current_balance = 0

    st.write(f"### الشهر الحالي: {current_date.strftime('%B %Y')}")
    st.write(f"### الرصيد المتبقي: {current_balance:.2f} ريال")
    st.write(f"### تاريخ الانتهاء المتوقع: {end_date.strftime('%B %Y')}")

    # Generate the repayment table
    st.subheader("جدول السداد القادم")
    table_data = []
    next_balance = current_balance
    next_month = current_date.replace(day=1) if current_balance > 0 else end_date

    for i in range(1, total_months + 1):  # Show until the mortgage is paid off
        next_balance -= monthly_payment
        if next_balance < 0:
            next_balance = 0
        table_data.append({
            "الشهر": next_month.strftime('%B %Y'),
            "السنة": next_month.year,  # Add year for yearly grouping
            "القسط الشهري (ريال)": monthly_payment,
            "الرصيد المتبقي (ريال)": round(next_balance, 2)
        })
        next_month += relativedelta(months=+1)
        if next_balance <= 0:
            break

    df = pd.DataFrame(table_data)
    st.table(df)

# Determine the correct key for the "Month" and "Year" columns based on language
month_key = "Month" if language == "English" else "الشهر"
year_key = "Year" if language == "English" else "السنة"
balance_key = "Remaining Balance (Riyals)" if language == "English" else "الرصيد المتبقي (ريال)"

# Group data by year
yearly_data = df.groupby(year_key).last().reset_index()

# Data for visualization
years = yearly_data[year_key].astype(str)  # Convert years to string for charts
balances = yearly_data[balance_key]

# 1. Line Chart for Remaining Balance Over Time
st.subheader("Remaining Balance Over Time")
st.line_chart(pd.DataFrame({"Remaining Balance": balances}, index=years))

# 2. Bar Chart for Monthly Payments (Yearly Representation)
st.subheader("Yearly Payment Progress")
st.bar_chart(pd.DataFrame({"Yearly Payment": [monthly_payment * 12] * len(years)}, index=years))

# 3. Pie Chart for Paid vs. Remaining Balance
st.subheader("Paid vs. Remaining Balance")
paid_balance = remaining_balance - current_balance
pie_data = pd.DataFrame({
    "Category": ["Paid", "Remaining"],
    "Amount": [paid_balance, current_balance]
})
fig_pie = px.pie(pie_data, values="Amount", names="Category", title="Paid vs Remaining Balance")
st.plotly_chart(fig_pie)

# 4. Cumulative Progress with an Area Chart
st.subheader("Cumulative Payment Progress")
cumulative_payments = yearly_data[balance_key].iloc[0] - balances  # Calculate cumulative payments
st.area_chart(pd.DataFrame({"Cumulative Payments": cumulative_payments, "Remaining Balance": balances}, index=years))

# 5. Gauge Chart for Mortgage Completion Progress
st.subheader("Mortgage Completion Progress")
progress = (paid_balance / remaining_balance) * 100 if remaining_balance > 0 else 100
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=progress,
    title={'text': "Mortgage Completion (%)"},
    gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "green"}}
))
st.plotly_chart(fig_gauge)

# 6. Timeline Chart for Payment Milestones (Yearly)
st.subheader("Payment Milestones Timeline")
timeline_data = pd.DataFrame({
    "Year": years,
    "Remaining Balance": balances
})
timeline_chart = alt.Chart(timeline_data).mark_line(point=True).encode(
    x='Year',
    y='Remaining Balance',
    tooltip=['Year', 'Remaining Balance']
).properties(title="Payment Milestones Timeline")
st.altair_chart(timeline_chart, use_container_width=True)
