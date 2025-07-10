# main.py
from utils.preprocess import load_and_preprocess

load_and_preprocess(
    pitcher_name="Shohei Ohtani",
    start_date="2023-04-01",
    end_date="2023-04-30",
    save_path="data/ohtani_apr2023_cleaned.csv"
)