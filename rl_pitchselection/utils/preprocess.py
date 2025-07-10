# utils/preprocess.py
from pybaseball import statcast
import pandas as pd

def load_and_preprocess(pitcher_name: str, start_date: str, end_date: str, save_path: str):
    data = statcast(start_dt=start_date, end_dt=end_date)
    data = data[data['player_name'] == pitcher_name]

    # Filter incomplete rows
    data = data[data['pitch_type'].notna() & data['events'].notna()]

    # Add reward column (simple version)
    out_events = ['strikeout', 'flyout', 'groundout', 'pop out', 'lineout', 'double_play']
    hit_events = ['single', 'double', 'triple', 'home_run']
    walk_events = ['walk', 'hit_by_pitch']
    data['reward'] = data['events'].apply(
        lambda x: 1 if x in out_events else -1 if x in hit_events + walk_events else 0
    )

    # Encode stance and pitch type
    data['stand_R'] = (data['stand'] == 'R').astype(int)
    data['stand_L'] = (data['stand'] == 'L').astype(int)
    pitch_types = ['FF', 'SL', 'CH', 'CU', 'SI']
    data = data[data['pitch_type'].isin(pitch_types)]
    data['pitch_type_encoded'] = data['pitch_type'].map({k: v for v, k in enumerate(pitch_types)})

    # Select features and save
    features = ['balls', 'strikes', 'on_1b', 'on_2b', 'on_3b', 'stand_R', 'stand_L', 'pitch_type_encoded', 'reward']
    data[features].to_csv(save_path, index=False)
