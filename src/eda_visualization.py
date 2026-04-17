# ============================================
# EDA & VISUALIZATION - EXPENSE TRACKER
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Improve plot style
sns.set(style="whitegrid")

def perform_eda(df):
    print("\n🔹 Starting Exploratory Data Analysis...\n")

    # ----------------------------------------
    # BASIC INFO
    # ----------------------------------------
    print("Dataset Shape:", df.shape)
    print("\nColumns:", df.columns)

    print("\n🔹 Summary Statistics:")
    print(df.describe())

    # ----------------------------------------
    # CATEGORY-WISE SPENDING
    # ----------------------------------------
    print("\n🔹 Category-wise Spending:")

    category_spending = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    print(category_spending)

    # BAR CHART
    plt.figure(figsize=(8,5))
    sns.barplot(x=category_spending.index, y=category_spending.values)
    plt.title("Category-wise Spending")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("outputs/category_bar_chart.png")
    plt.show()

    # PIE CHART
    plt.figure(figsize=(6,6))
    plt.pie(category_spending, labels=category_spending.index, autopct='%1.1f%%')
    plt.title("Spending Distribution by Category")
    plt.savefig("outputs/category_pie_chart.png")
    plt.show()

    # ----------------------------------------
    # MONTHLY INCOME VS EXPENSE
    # ----------------------------------------
    print("\n🔹 Monthly Trends:")

    # If no Income column, create dummy (for project demo)
    if 'Income' not in df.columns:
        df['Income'] = df['Amount'] * 1.5   # simulated income

    monthly_data = df.groupby('Month')[['Amount', 'Income']].sum()

    print(monthly_data)

    # LINE CHART
    plt.figure(figsize=(8,5))
    sns.lineplot(data=monthly_data, markers=True)
    plt.title("Monthly Income vs Expense")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.savefig("outputs/monthly_income_vs_expense.png")
    plt.show()

    # ----------------------------------------
    # TRANSACTIONS BY WEEKDAY
    # ----------------------------------------
    print("\n🔹 Transactions by Weekday:")

    weekday_counts = df['Weekday'].value_counts()

    print(weekday_counts)

    # BAR CHART
    plt.figure(figsize=(8,5))
    sns.barplot(x=weekday_counts.index, y=weekday_counts.values)
    plt.title("Transactions by Weekday")
    plt.xticks(rotation=45)
    plt.savefig("outputs/weekday_transactions.png")
    plt.show()

    # ----------------------------------------
    # EXTRA INSIGHTS
    # ----------------------------------------
    print("\n🔹 Additional Insights:")

    print("Top Spending Category:", category_spending.idxmax())
    print("Lowest Spending Category:", category_spending.idxmin())
    print("Total Expense:", df['Amount'].sum())

    print("\n✅ EDA Completed Successfully!")