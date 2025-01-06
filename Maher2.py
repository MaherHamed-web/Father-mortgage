import streamlit as st
from datetime import datetime, timedelta

# Set the initial mortgage details
remaining_balance = 168000  # Initial remaining mortgage in Riyals
monthly_payment = 1667      # Monthly payment in Riyals
start_date = datetime(2025, 1, 1)  # Assume payments start January 2025

# Calculate the total months and end date
total_months = remaining_balance // monthly_payment
end_date = start_date + timedelta(days=total_months * 30)

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
