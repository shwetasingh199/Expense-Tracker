# ============================================
# DATA CLEANING & PREPROCESSING MODULE
# ============================================

import pandas as pd

def clean_expense_data(file_path):
    print("🔹 Loading dataset...")
    
    df = pd.read_csv(file_path)

    print("\n🔹 Original Dataset:")
    print(df.head())

    # ----------------------------------------
    # 1. HANDLE MISSING VALUES
    # ----------------------------------------
    print("\n🔹 Checking missing values...")
    print(df.isnull().sum())

    # Fill missing Category with 'Unknown'
    df['Category'] = df['Category'].fillna('Unknown')

    # Fill missing Payment Method
    df['Payment Method'] = df['Payment Method'].fillna('Unknown')

    # Fill missing Amount with median
    df['Amount'] = df['Amount'].fillna(df['Amount'].median())

    # Drop rows where Date is missing (important field)
    df = df.dropna(subset=['Date'])

    print("\n✅ Missing values handled!")

    # ----------------------------------------
    # 2. STANDARDIZE TEXT (Category & Payment)
    # ----------------------------------------
    print("\n🔹 Standardizing text...")

    df['Category'] = df['Category'].str.strip().str.title()
    df['Payment Method'] = df['Payment Method'].str.strip().str.upper()

    print("\nUnique Categories:", df['Category'].unique())
    print("Unique Payment Methods:", df['Payment Method'].unique())

    # ----------------------------------------
    # 3. CONVERT DATA TYPES
    # ----------------------------------------
    print("\n🔹 Converting data types...")

    # Convert Date column
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Convert Amount to numeric
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

    # Remove invalid rows after conversion
    df = df.dropna(subset=['Date', 'Amount'])

    print("\n✅ Data types converted!")

    # ----------------------------------------
    # 4. REMOVE DUPLICATES
    # ----------------------------------------
    print("\n🔹 Removing duplicates...")

    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    print(f"Removed {before - after} duplicate rows")

    # ----------------------------------------
    # 5. FEATURE ENGINEERING
    # ----------------------------------------
    print("\n🔹 Creating new features...")

    df['Month'] = df['Date'].dt.month
    df['Month Name'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    df['Weekday'] = df['Date'].dt.day_name()

    print("\n✅ New columns added!")

    # ----------------------------------------
    # 6. FINAL CLEAN DATA PREVIEW
    # ----------------------------------------
    print("\n🔹 Cleaned Dataset Preview:")
    print(df.head())

    print("\n🔹 Final Dataset Info:")
    print(df.info())

    return df


# ----------------------------------------
# TEST RUN (Only when running this file directly)
# ----------------------------------------
if __name__ == "__main__":
    cleaned_df = clean_expense_data("data/expenses.csv")

    # Save cleaned data
    cleaned_df.to_csv("data/cleaned_expenses.csv", index=False)

    print("\n📁 Cleaned data saved to data/cleaned_expenses.csv")