import pandas as pd
import argparse
import os as os

from config_pages import get_db
from pathlib import Path

parser = argparse.ArgumentParser(description="Add members from a CSV file")
parser.add_argument("csv_file", type=str, help="Path to the CSV file")
args = parser.parse_args()

csv_file = Path(args.csv_file)
if not csv_file.is_file():
    raise FileNotFoundError(f"CSV file does not exist: {csv_file}")

# Reads an excel file 
data_df = pd.read_excel(
    csv_file,
    names=["english_name", "chinese_name", "index", "family_name"]
)
# Strip white spaces at the ends of string
data_df["english_name"] = data_df["english_name"].str.strip()
data_df["chinese_name"] = data_df["chinese_name"].str.replace(r"\s+", "", regex=True)

# Add families to database
families = data_df[["index", "family_name"]].drop_duplicates()
db = get_db()
family_ids = []
for _, row in families.iterrows():
    family_ids.append(db.add_family(row.family_name))
families["family_id"] = family_ids
data_df = data_df.merge(families[["index", "family_id"]], on='index', how='inner')

# Add members to database
db = get_db()
for _, row in data_df.iterrows():
    member_data = [row.english_name, row.chinese_name] + [""] * 7 + [row.family_id]
    db.add_member(member_data)