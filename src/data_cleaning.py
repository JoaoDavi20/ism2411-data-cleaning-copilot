# This script cleans the sales data by standardizing column names and removing invalid values
# This is important to make the data readble

import pandas as pd

# Load csv file
df = pd.read_csv("data/raw/sales_data_raw.csv")

# Standardize column names
# What: Convert all column names to lowercase and replace spaces with underscores
# Why: Makes it easier to read
df.columns = df.columns.str.strip().str.lower().str.replace(' ','_')

# Strip leading/trailing whitespace from product names and categories and capitalizes them
# What: Remove extra spaces from text fields and capitalize them properly
# Why: Those incconsistencies can cause issues when reading it
df["prodname"] = df["prodname"].astype(str).str.strip().str.title()
df["category"] = df["category"].astype(str).str.strip().str.title()

# Handle missing prices and quantities
# What: Remove rows with missing price or quantity values
# Why: These values are essential for sales analysis and calculations
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["qty"] = pd.to_numeric(df["qty"], errors="coerce")
df = df.dropna(subset=["price", "qty"])

# Remove rows with clearly invalid values
# What : Remove rows with negative quantities and prices
# Why: Because they do not make sense in real life
df =df[df["qty"] > 0]
df =df[df["price"] > 0]

# AI (CoPilot) Section:

# Create function to calculate total profit from each item sold
def calculate_total_profit(row):
    return round(row["price"] * row["qty"],2)

# The IA did not generated the function but it did not added anything to the data
# The IA also did not round the values, which make the data look weird
df["total_profit"] = df.apply(calculate_total_profit, axis=1)


def clean_column_names(df):
    """
    Cleans column names by converting to lowercase, stripping whitespace,
    and replacing spaces with underscores.
    """
    df.columns = df.columns.str.strip().str.title().str.replace(' ', '_')
    return df

# Again IA did not applied the function
# Also, as we can see in the comment, it coverted to lowercase, which I do not believe is the best choice, so I changed to title case
df = clean_column_names(df)

# Export cleaned data to a new CSV file
output_file_path = "data/processed/sales_data_clean.csv"
df.to_csv(output_file_path, index=False)

print("Cleaning complete. First few rows:")
print(df.head())