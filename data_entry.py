import pandas as pd
from config_pages import get_db

# Reads an excel file 
data_df = pd.read_excel(
    "TSA attendance 2026.xlsx",
    names=["english_name", "chinese_name"]
)

# Strip white spaces at the ends of string
data_df["english_name"] = data_df["english_name"].str.strip()
data_df["chinese_name"] = data_df["chinese_name"].str.replace(r"\s+", "", regex=True)

# Add members to database
db = get_db()
for row in data_df.itertuples(index=False):
    db.add_member(row.english_name, row.chinese_name)