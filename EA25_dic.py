import json
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import BytesIO
from difflib import get_close_matches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

try:
    # convert the content of the file to python object
    data = json.load(open("players.json"))
except FileNotFoundError:
    print("The file was not found, please try again")
    exit()
# create dictionary while saved the players by name
data_dict = {player['Name'].lower(): player for player in data}


def translate(choice):
    word = choice.lower()

    matches = [name for name in data_dict.keys() if word in name.lower()]
    if matches:
        return data_dict[matches[0]]

    close_matches = get_close_matches(word, data_dict.keys())

    if close_matches:
        suggested = close_matches[0]
        print(f"did you mean '{suggested}' instead? ")
        decide = input("press y for yes or n for no: ")
        if decide == "y":
            return data_dict[suggested]
        elif decide == "n":
            return
        else:
            return "Invalid input, please only y or n "

    return "The player does not exist."

def get_player_image_url(player_name):
    api_url = f"https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={player_name.replace(' ', '%20')}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if 'player' in data and data['player']:
            player_data = data['player'][0]
            if 'strCutout' in player_data:
                return player_data['strCutout']
            else:
                print(f"Image not found for {player_name}")
        else:
            print(f"No image foung for {player_name}")
            return None
    else:
        print(f"Error fetching image for {player_name}")
        return None
    
    return None
    
            
        

def plot_player(player, img_url):
    state = {
        'Overall Rating' : player['OVR'],
        'Speed' : player['PAC'],
        'Shooting': player['SHO'],
        'Passing' : player['PAS'],
        'Dribbling' : player['DRI'],
        'Defending' : player['DEF'],
        'Physical' : player['PHY']
    }
    
    df = pd.DataFrame(list(state.items()), columns=['Parameters', 'Value'])
    plt.figure(figsize=(10,5))
    plt.bar(df['Parameters'], df['Value'], color='lightblue')
    plt.style.use('dark_background')
    plt.xlabel('Parametes')
    plt.ylabel('Values')
    plt.title(f"Player Statistics: {player['Name']} - {player['Team']}")
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    if img_url:
        # Downloading and opening the image
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        
        # Creating and presenting the image box
        imagebox = OffsetImage(img, zoom=0.1)
        ab = AnnotationBbox(imagebox, (0.5, 0.7), frameon=False, xycoords='axes fraction')
        
        # Getting the plot
        ax = plt.gca()
        ax.add_artist(ab)
    else:
        print("No image available for this player.")
    
    plt.show()    
    
    


print("Hi, this is the new FIFA 2025 dictionary!\n")
while True:
    choice = input("Search a player or -1 to exit: ")
    if choice != "-1":
        result = translate(choice)
        # check if the input exist in the dictinary
        if isinstance(result, dict):
            print(f"Player found: {result['Name']}")
            print(f"- Team: {result['Team']} - Age: {result['Age']} \n")
            img_url = get_player_image_url(result['Name'])
            plot_player(result, img_url)
        else:
            print("The player does not exsit.")
    else:
        break