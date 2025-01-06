# Determine the correct key for the "Month" column based on language
month_key = "Month" if language == "English" else "الشهر"
balance_key = "Remaining Balance (Riyals)" if language == "English" else "الرصيد المتبقي (ريال)"

# Data for visualization: Remaining balance over time
months = [row[month_key] for row in table_data]
balances = [row[balance_key] for row in table_data]

# 1. Line Chart for Remaining Balance Over Time
st.subheader("Remaining Balance Over Time")
st.line_chart(pd.DataFrame({"Remaining Balance": balances}, index=months))

# 2. Bar Chart for Monthly Payments
st.subheader("Monthly Payment Progress")
st.bar_chart(pd.DataFrame({"Monthly Payment": [monthly_payment] * len(months)}, index=months))

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
cumulative_payments = [monthly_payment * (i + 1) for i in range(len(months))]
st.area_chart(pd.DataFrame({"Cumulative Payments": cumulative_payments, "Remaining Balance": balances}, index=months))

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

# 6. Timeline Chart for Payment Milestones
st.subheader("Payment Milestones Timeline")
timeline_data = pd.DataFrame({
    "Month": months,
    "Remaining Balance": balances
})
timeline_chart = alt.Chart(timeline_data).mark_line(point=True).encode(
    x='Month',
    y='Remaining Balance',
    tooltip=['Month', 'Remaining Balance']
).properties(title="Payment Milestones Timeline")
st.altair_chart(timeline_chart, use_container_width=True)
