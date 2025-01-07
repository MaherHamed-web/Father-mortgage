import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta  # To handle month-by-month increments

# خريطة أسماء الأشهر العربية
arabic_months = {
    "January": "يناير",
    "February": "فبراير",
    "March": "مارس",
    "April": "أبريل",
    "May": "مايو",
    "June": "يونيو",
    "July": "يوليو",
    "August": "أغسطس",
    "September": "سبتمبر",
    "October": "أكتوبر",
    "November": "نوفمبر",
    "December": "ديسمبر"
}

# تحويل اسم الشهر إلى اللغة العربية
def get_arabic_month(date):
    english_month = date.strftime('%B')  # Get the month in English
    return arabic_months[english_month]

# إضافة التبديل لتعديل الأرقام
st.title("متابعة سداد الرهن العقاري")
st.markdown("<hr>", unsafe_allow_html=True)  # Add a horizontal line for clarity

toggle_edit = st.checkbox("تعديل الأرقام")  # Toggle to enable/disable editing

# الأرقام الافتراضية
default_original_amount = 500000  # الرصيد الأصلي (ريال)
default_remaining_balance = 168000  # الرصيد المتبقي (ريال)
default_monthly_payment = 1667  # القسط الشهري (ريال)

if toggle_edit:
    # عند تشغيل التبديل يمكن تعديل الأرقام
    original_amount = st.number_input("الرصيد الأصلي (ريال)", value=default_original_amount, step=1000)
    remaining_balance = st.number_input("الرصيد المتبقي (ريال)", value=default_remaining_balance, step=1000)
    monthly_payment = st.number_input("القسط الشهري (ريال)", value=default_monthly_payment, step=100)
else:
    # في الحالة العادية استخدم الأرقام الافتراضية
    original_amount = default_original_amount
    remaining_balance = default_remaining_balance
    monthly_payment = default_monthly_payment

# حساب عدد الأشهر الإجمالي وتاريخ الانتهاء
total_months = original_amount // monthly_payment
end_date = datetime.now() + relativedelta(months=+(total_months - (original_amount - remaining_balance) // monthly_payment))

# عرض التفاصيل بخطوط كبيرة
st.markdown("### الرصيد الأصلي")
st.markdown(f"<p style='font-size:24px; font-weight:bold;'>{original_amount:,.2f} ريال</p>", unsafe_allow_html=True)

st.markdown("### الشهر الحالي")
st.markdown(f"<p style='font-size:24px; font-weight:bold;'>{get_arabic_month(datetime.now())} {datetime.now().year}</p>", unsafe_allow_html=True)

st.markdown("### الرصيد المتبقي")
st.markdown(f"<p style='font-size:24px; font-weight:bold;'>{remaining_balance:,.2f} ريال</p>", unsafe_allow_html=True)

st.markdown("### تاريخ الانتهاء المتوقع")
st.markdown(f"<p style='font-size:24px; font-weight:bold;'>{get_arabic_month(end_date)} {end_date.year}</p>", unsafe_allow_html=True)

# الرسم الدائري للرصيد المدفوع والمتبقي
st.subheader("النسبة بين المدفوع والمتبقي")
paid_balance = original_amount - remaining_balance
pie_data = pd.DataFrame({
    "الفئة": ["المدفوع", "المتبقي"],
    "المبلغ": [paid_balance, remaining_balance]
})
fig_pie = px.pie(pie_data, values="المبلغ", names="الفئة", title="النسبة بين المدفوع والمتبقي")
st.plotly_chart(fig_pie, use_container_width=True)

# مقياس نسبة اكتمال الرهن العقاري
st.subheader("نسبة اكتمال الرهن العقاري")
progress = (paid_balance / original_amount) * 100 if original_amount > 0 else 100
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=progress,
    title={'text': "نسبة الاكتمال (%)"},
    gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "green"}}
))
st.plotly_chart(fig_gauge, use_container_width=True)

# الخط الزمني للرصيد المتبقي
st.subheader("الخط الزمني للرصيد المتبقي")
table_toggle = st.checkbox("عرض جدول السداد الكامل")  # Toggle to show/hide table
if table_toggle:
    table_data = []
    next_balance = remaining_balance
    next_month = datetime.now().replace(day=1)

    for i in range(1, total_months + 1):  # حتى اكتمال سداد الرهن
        next_balance -= monthly_payment
        if next_balance < 0:
            next_balance = 0
        table_data.append({
            "السنة": next_month.year,
            "الشهر": f"{get_arabic_month(next_month)} {next_month.year}",
            "القسط الشهري (ريال)": monthly_payment,
            "الرصيد المتبقي (ريال)": round(next_balance, 2)
        })
        next_month += relativedelta(months=+1)
        if next_balance <= 0:
            break

    df = pd.DataFrame(table_data)
    st.table(df)
