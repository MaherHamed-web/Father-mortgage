import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from dateutil.relativedelta import relativedelta  # To handle month-by-month increments

# تفاصيل الرهن العقاري
remaining_balance = 168000  # الرصيد المتبقي (ريال)
monthly_payment = 1667      # القسط الشهري (ريال)
start_date = datetime(2025, 1, 1)  # بداية السداد

# حساب عدد الأشهر الإجمالي وتاريخ الانتهاء
total_months = remaining_balance // monthly_payment
end_date = start_date + relativedelta(months=+total_months)

# عرض العنوان والتفاصيل
st.title("متابعة سداد الرهن العقاري")
st.subheader("تفاصيل الرهن العقاري")

# حساب الرصيد المتبقي بناءً على الشهر الحالي
current_date = datetime.now()
elapsed_months = ((current_date.year - start_date.year) * 12) + (current_date.month - start_date.month)
current_balance = remaining_balance - (elapsed_months * monthly_payment)

if current_balance < 0:
    current_balance = 0

st.write(f"### الشهر الحالي: {current_date.strftime('%B %Y')}")
st.write(f"### الرصيد المتبقي: {current_balance:.2f} ريال")
st.write(f"### تاريخ الانتهاء المتوقع: {end_date.strftime('%B %Y')}")

# إنشاء جدول السداد القادم
st.subheader("جدول السداد القادم")
table_data = []
next_balance = current_balance
next_month = current_date.replace(day=1) if current_balance > 0 else end_date

for i in range(1, total_months + 1):  # حتى اكتمال سداد الرهن
    next_balance -= monthly_payment
    if next_balance < 0:
        next_balance = 0
    table_data.append({
        "السنة": next_month.year,
        "الشهر": next_month.strftime('%B %Y'),
        "القسط الشهري (ريال)": monthly_payment,
        "الرصيد المتبقي (ريال)": round(next_balance, 2)
    })
    next_month += relativedelta(months=+1)
    if next_balance <= 0:
        break

df = pd.DataFrame(table_data)
st.table(df)

# تجميع البيانات حسب السنة
yearly_data = df.groupby("السنة").last().reset_index()

# بيانات للرسم البياني
years = yearly_data["السنة"].astype(str)
balances = yearly_data["الرصيد المتبقي (ريال)"]

# 1. الرسم الخطي للرصيد المتبقي
st.subheader("الرصيد المتبقي عبر السنوات")
st.line_chart(pd.DataFrame({"الرصيد المتبقي": balances}, index=years))

# 2. الرسم البياني للأقساط السنوية
st.subheader("تقدم السداد السنوي")
st.bar_chart(pd.DataFrame({"القسط السنوي": [monthly_payment * 12] * len(years)}, index=years))

# 3. الرسم الدائري للرصيد المدفوع والمتبقي
st.subheader("النسبة بين المدفوع والمتبقي")
paid_balance = remaining_balance - current_balance
pie_data = pd.DataFrame({
    "الفئة": ["المدفوع", "المتبقي"],
    "المبلغ": [paid_balance, current_balance]
})
fig_pie = px.pie(pie_data, values="المبلغ", names="الفئة", title="النسبة بين المدفوع والمتبقي")
st.plotly_chart(fig_pie)

# 4. الرسم البياني التراكمي للسداد
st.subheader("التقدم التراكمي للسداد")
cumulative_payments = yearly_data["الرصيد المتبقي (ريال)"].iloc[0] - balances  # حساب السداد التراكمي
st.area_chart(pd.DataFrame({"السداد التراكمي": cumulative_payments, "الرصيد المتبقي": balances}, index=years))

# 5. مقياس نسبة اكتمال الرهن العقاري
st.subheader("نسبة اكتمال الرهن العقاري")
progress = (paid_balance / remaining_balance) * 100 if remaining_balance > 0 else 100
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=progress,
    title={'text': "نسبة الاكتمال (%)"},
    gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "green"}}
))
st.plotly_chart(fig_gauge)

# 6. الخط الزمني للرصيد المتبقي
st.subheader("الخط الزمني للرصيد المتبقي")
timeline_data = pd.DataFrame({
    "السنة": years,
    "الرصيد المتبقي": balances
})
timeline_chart = alt.Chart(timeline_data).mark_line(point=True).encode(
    x='السنة',
    y='الرصيد المتبقي',
    tooltip=['السنة', 'الرصيد المتبقي']
).properties(title="الخط الزمني للرصيد المتبقي")
st.altair_chart(timeline_chart, use_container_width=True)
