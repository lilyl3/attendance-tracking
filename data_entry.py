import pandas as pd
import argparse
import os as os

from config_pages import get_db
from pathlib import Path

parser = argparse.ArgumentParser(description="Add members from an Excel file")
parser.add_argument("xslx_file", type=str, help="Path to an Excel file")
args = parser.parse_args()

xslx_file = Path(args.xslx_file)
if not xslx_file.is_file():
    raise FileNotFoundError(f"xslx file does not exist: {xslx_file}")

# Reads an excel file 
data_df = pd.read_excel(
    xslx_file,
    names=["english_name", "chinese_name"]
)

# Strip white spaces at the ends of string
data_df["english_name"] = data_df["english_name"].str.strip()
data_df["chinese_name"] = data_df["chinese_name"].str.replace(r"\s+", "", regex=True)

# Add members to database
db = get_db()
for row in data_df.itertuples(index=False):
    db.add_member(row.english_name, row.chinese_name)