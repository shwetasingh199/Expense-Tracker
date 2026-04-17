# ===============================================
# EXPENSE TRACKER - COMPLETE ANALYSIS SCRIPT
# ===============================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set(style="whitegrid")

# -----------------------------------------------
# STEP 1: LOAD + TRANSFORM DATASET 
# -----------------------------------------------
print("Loading dataset...")

df = pd.read_csv("data/expenses.csv")

# Clean column names
df.columns = df.columns.str.strip()

print("\n🔹 Transforming dataset...")

# YOUR DATASET EXPENSE COLUMNS 
expense_cols = [
    'Food', 'Groceries', 'Transport', 'Entertainment',
    'Shopping', 'Rent', 'Bills', 'Healthcare', 'Education'
]

# Convert wide → long format
df = df.melt(
    id_vars=['UserID', 'Year', 'Month'],
    value_vars=expense_cols,
    var_name='Category',
    value_name='Amount'
)

# Create Date column
df['Date'] = pd.to_datetime(
    df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-01'
)

# Add Payment Method (dummy)
df['Payment Method'] = np.random.choice(
    ['UPI', 'Cash', 'Card'],
    size=len(df)
)

# Keep only required columns
df = df[['Date', 'Category', 'Amount', 'Payment Method']]

# Remove zero or negative values
df = df[df['Amount'] > 0]

print("✅ Transformation Completed!")
# -----------------------------------------------
# STEP 2: DATA PREVIEW
# -----------------------------------------------
print("\n🔹 First 5 Rows:")
print(df.head())

print("\n🔹 Last 5 Rows:")
print(df.tail())

# -----------------------------------------------
# STEP 3: DATASET STRUCTURE
# -----------------------------------------------
print("\n🔹 Dataset Info:")
df.info()

print("\n🔹 Shape of Dataset:")
print(df.shape)

print("\n🔹 Column Names:")
print(df.columns)

# -----------------------------------------------
# STEP 4: CHECK MISSING VALUES
# -----------------------------------------------
print("\n🔹 Missing Values:")
print(df.isnull().sum())

# -----------------------------------------------
# STEP 5: UNIQUE VALUES
# -----------------------------------------------
print("\n🔹 Unique Categories:")
print(df['Category'].unique())

print("\n🔹 Unique Payment Methods:")
print(df['Payment Method'].unique())

# -----------------------------------------------
# STEP 6: SUMMARY STATISTICS
# -----------------------------------------------
print("\n🔹 Statistical Summary:")
print(df.describe())

# -----------------------------------------------
# STEP 7: VALUE COUNTS
# -----------------------------------------------
print("\n🔹 Category Count:")
print(df['Category'].value_counts())

print("\n🔹 Payment Method Count:")
print(df['Payment Method'].value_counts())

# -----------------------------------------------
# STEP 8: DATA CLEANING
# -----------------------------------------------
print("\n🔹 Cleaning Data...")

# Handle missing values
df['Category'] = df['Category'].fillna('Unknown')
df['Payment Method'] = df['Payment Method'].fillna('Unknown')
df['Amount'] = df['Amount'].fillna(df['Amount'].median())
df = df.dropna(subset=['Date'])

# Standardize text
df['Category'] = df['Category'].str.strip().str.title()
df['Payment Method'] = df['Payment Method'].str.strip().str.upper()

# Convert data types
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

# Drop invalid rows
df = df.dropna(subset=['Date', 'Amount'])

# Remove duplicates
df = df.drop_duplicates()

print("✅ Data Cleaning Completed!")

# -----------------------------------------------
# STEP 9: FEATURE ENGINEERING
# -----------------------------------------------
print("\n🔹 Creating New Features...")

df['Month'] = df['Date'].dt.month
df['Month Name'] = df['Date'].dt.month_name()
df['Day'] = df['Date'].dt.day
df['Weekday'] = df['Date'].dt.day_name()

print("✅ Features Added!")

# -----------------------------------------------
# STEP 10: SAVE CLEANED DATA
# -----------------------------------------------
df.to_csv("data/cleaned_expenses.csv", index=False)
print("\n📁 Cleaned dataset saved!")

# -----------------------------------------------
# STEP 11: EDA ANALYSIS
# -----------------------------------------------
print("\n🔹 Performing EDA...")

# Category-wise spending
category_spending = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
print("\nCategory-wise Spending:")
print(category_spending)

# Monthly spending
monthly_spending = df.groupby('Month Name')['Amount'].sum()

# Correct order of months
monthly_spending = monthly_spending.reindex([
    'January','February','March','April','May','June',
    'July','August','September','October','November','December'
])
print("\nMonthly Spending:")
print(monthly_spending)

# Weekday transactions
weekday_counts = df['Weekday'].value_counts()
print("\nTransactions by Weekday:")
print(weekday_counts)

# -----------------------------------------------
# STEP 12: VISUALIZATION
# -----------------------------------------------

# Category Bar Chart
plt.figure(figsize=(8,5))
sns.barplot(x=category_spending.index, y=category_spending.values)
plt.title("Category-wise Spending")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/category_bar_chart.png")
plt.show()

# Pie Chart
plt.figure(figsize=(6,6))
plt.pie(category_spending, labels=category_spending.index, autopct='%1.1f%%')
plt.title("Spending Distribution")
plt.savefig("outputs/category_pie_chart.png")
plt.show()

# Monthly Line Chart
plt.figure(figsize=(8,5))
sns.lineplot(x=monthly_spending.index, y=monthly_spending.values, marker='o')
plt.title("Monthly Spending Trend")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.savefig("outputs/monthly_trend.png")
plt.show()

# Weekday Chart
plt.figure(figsize=(8,5))
sns.barplot(x=weekday_counts.index, y=weekday_counts.values)
plt.title("Transactions by Weekday")
plt.xticks(rotation=45)
plt.savefig("outputs/weekday_transactions.png")
plt.show()

# -----------------------------------------------
# STEP 13: FINAL INSIGHTS
# -----------------------------------------------
print("\n🔹 Final Insights:")

print("Top Spending Category:", category_spending.idxmax())
print("Lowest Spending Category:", category_spending.idxmin())
print("Total Spending:", df['Amount'].sum())

print("\n🎉 PROJECT COMPLETED SUCCESSFULLY!")