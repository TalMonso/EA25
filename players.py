import pandas as pd
import json

try:
    df = pd.read_csv("all_players.csv", low_memory=False)
except FileNotFoundError:
    print("File are not found")
    exit()

try:      
    players_json = df.to_json(orient="records", indent=4)
    with open("players.json", "w") as json_file:
        json_file.write(players_json)
except IOError:
    print("IOError")

