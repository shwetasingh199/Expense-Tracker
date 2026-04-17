# -----------------------------------------------
# TRANSFORM KAGGLE DATA (FIXED VERSION)
# -----------------------------------------------
print("\n🔹 Transforming dataset...")

# Clean column names (IMPORTANT)
df.columns = df.columns.str.strip()

print("Available Columns:", df.columns)

# Select only columns that actually exist
possible_cols = [
    'Food', 'Groceries', 'Transport', 'Entertainment',
    'Shopping', 'Rent', 'Bills', 'Healthcare', 'Education'
]

expense_cols = [col for col in possible_cols if col in df.columns]

print("Using Expense Columns:", expense_cols)

# Melt only if columns exist
if len(expense_cols) == 0:
    print("❌ No expense columns found! Check dataset.")
else:
    df = df.melt(
        id_vars=['UserID', 'Year', 'Month'],
        value_vars=expense_cols,
        var_name='Category',
        value_name='Amount'
    )

    # Convert Amount safely
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

    # Create Date
    df['Date'] = pd.to_datetime(
        df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-01',
        errors='coerce'
    )

    # Add Payment Method
    df['Payment Method'] = 'UPI'

    # Keep required columns
    df = df[['Date', 'Category', 'Amount', 'Payment Method']]

    # ❗ FIX: DO NOT REMOVE ALL ROWS
    df = df[df['Amount'].notnull()]   # only remove NaN, NOT zero

    print("\nTransformed Data Preview:")
    print(df.head())

    print("Total Rows After Transformation:", len(df))

    print("✅ Transformation Completed!")