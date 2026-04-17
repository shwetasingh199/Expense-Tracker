# ===============================================
# STREAMLIT DASHBOARD - EXPENSE TRACKER
# ===============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# -----------------------------------------------
# PAGE CONFIG
# -----------------------------------------------
st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("💰 Expense Tracker")
st.markdown("---")

# -----------------------------------------------
# LOAD DATA
# -----------------------------------------------
# -----------------------------------------------
# LOAD DATA
# -----------------------------------------------
@st.cache_data
def load_data():
    import os
    import pandas as pd
    import streamlit as st

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "cleaned_expenses.csv")

    # Check if file exists
    if not os.path.exists(file_path):
        st.error("❌ File not found! Run main.py first.")
        st.stop()

    # Check if file is empty
    if os.stat(file_path).st_size == 0:
        st.error("❌ File is empty! Please regenerate data.")
        st.stop()

    df = pd.read_csv(file_path)

    if df.empty:
        st.error("❌ Dataset has no rows!")
        st.stop()

    df['Date'] = pd.to_datetime(df['Date'])

    return df

# ✅ THIS LINE IS VERY IMPORTANT
df = load_data()
# -----------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------
st.sidebar.header("🔎 Filters")

categories = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

# Month filter
months = st.sidebar.multiselect(
    "Select Month",
    options=df['Month'].unique(),
    default=df['Month'].unique()
)

# Apply filters
filtered_df = df[
    (df['Category'].isin(categories)) &
    (df['Month'].isin(months))
]

# -----------------------------------------------
# KPI METRICS
# -----------------------------------------------
st.subheader("📊 Key Metrics")

# -------------------------------
# KPI CALCULATIONS
# -------------------------------
total_spending = round(filtered_df['Amount'].sum(), 2)
avg_spending = round(filtered_df['Amount'].mean(), 2)

total_income = round(total_spending * 1.5, 2)  # dummy logic
savings = round(total_income - total_spending, 2)

# -------------------------------
# DISPLAY METRICS
# -------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Spending", f"₹ {total_spending:,.2f}")
col2.metric("Transactions", len(filtered_df))
col3.metric("Avg Spending", f"₹ {avg_spending:,.2f}")
col4.metric("Income", f"₹ {total_income:,.2f}")

if savings >= 0:
    col5.metric("Savings", f"₹ {savings:,.2f}", delta="Good")
else:
    col5.metric("Savings", f"₹ {savings:,.2f}", delta="Overspending ⚠️")
# -----------------------------------------------
# CATEGORY-WISE BAR CHART
# -----------------------------------------------
st.subheader("📊 Category-wise Spending")

category_spending = filtered_df.groupby('Category')['Amount'].sum()

fig1, ax1 = plt.subplots(figsize=(8,5))
sns.barplot(x=category_spending.index, y=category_spending.values, ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

# -----------------------------------------------
# PIE CHART
# -----------------------------------------------
st.subheader("🥧 Spending Distribution")

fig2, ax2 = plt.subplots()
ax2.pie(category_spending, labels=category_spending.index, autopct='%1.1f%%')
st.pyplot(fig2)

# -----------------------------------------------
# MONTHLY TREND LINE CHART
# -----------------------------------------------
st.subheader("📈 Monthly Spending Trend")

monthly_spending = filtered_df.groupby('Month Name')['Amount'].sum()

monthly_spending = monthly_spending.reindex([
    'January','February','March','April','May','June',
    'July','August','September','October','November','December'
])

fig3, ax3 = plt.subplots(figsize=(8,5))
sns.lineplot(x=monthly_spending.index, y=monthly_spending.values, marker='o', ax=ax3)
ax3.set_xlabel("Month")
ax3.set_ylabel("Amount")
st.pyplot(fig3)

# -----------------------------------------------
# WEEKDAY ANALYSIS
# -----------------------------------------------
st.subheader("📅 Transactions by Weekday")

weekday_counts = filtered_df['Weekday'].value_counts()

fig4, ax4 = plt.subplots(figsize=(8,5))
sns.barplot(x=weekday_counts.index, y=weekday_counts.values, ax=ax4)
plt.xticks(rotation=45)
st.pyplot(fig4)

# -----------------------------------------------
# DATA TABLE
# -----------------------------------------------
st.subheader("📄 Filtered Data")
st.dataframe(filtered_df)

# -----------------------------------------------
# FOOTER
# -----------------------------------------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")