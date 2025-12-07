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
df =df[df["qty"] >= 0]
df =df[df["price"] >= 0]

# Export cleaned data to a new CSV file
output_file_path = "data/processed/sales_data_clean.csv"
df.to_csv(output_file_path, index=False)