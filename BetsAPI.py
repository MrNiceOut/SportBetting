import requests
import csv
import json
import tkinter as tk
import GameData as GD
import pprint
import datetime
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import messagebox

# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = '45779c083e2ad88fbea92c4a2e2b0f89'

SPORT = 'americanfootball_nfl' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'decimal' # decimal | american

DATE_FORMAT = 'iso' # iso | unix

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# First get a list of in-season sports
#   The sport 'key' from the response can be used to get odds in the next request
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# sports_response = requests.get(
#     'https://api.the-odds-api.com/v4/sports', 
#     params={
#         'api_key': API_KEY
#     }
# )


# if sports_response.status_code != 200:
#     print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

# else:
#     print('List of in season sports:', sports_response.json())



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
# This will deduct from the usage quota
# The usage quota cost = [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
    exit()
else:
    odds_json = odds_response.json()
    
    # Get the current date
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_datetime_for_filename = current_datetime.replace(":", "_")
    # Load JSON data from a file into a dictionary
    json_filename = f'odds_data_{current_datetime_for_filename}.json'
    with open(json_filename, 'w') as jsonfile:
        json.dump(odds_json, jsonfile, indent=4)

    print(f'Odds data has been saved to {json_filename}')

# Check the usage quota
print('Remaining requests', odds_response.headers['x-requests-remaining'])
print('Used requests', odds_response.headers['x-requests-used'])


    
# Get the directory containing the JSON files
directory = "/Users/Chris/Documents/Python_Codes/Bets"

# List all files in the directory
all_files = os.listdir(directory)

# Filter JSON files and sort them by name
json_files = [file for file in all_files if file.startswith('odds_data_') and file.endswith('.json')]
json_files.sort()

# Get the last 5 JSON files
last_5_files = json_files[-10:]

with open(json_filename) as jsonfile:
    data = json.load(jsonfile)

#----------------------------------------------------------------------------------------------------
# Create the main window
root = tk.Tk()
root.geometry('700x900')
# Create a label for the file name
label = tk.Label(root, text="NFL Odds Data")
label.pack()

# Create a label to display the list of events
events_label = tk.Label(root, text="Events:")
events_label.pack()

# Create a scrolled text widget to display the event list
event_list_text = tk.Text(root, wrap="none")
event_list_text.pack(fill="both", expand=True)

# Create a vertical scrollbar for the event list
scrollbar = tk.Scrollbar(event_list_text)
scrollbar.pack(side="right", fill="y")
event_list_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=event_list_text.yview)

event_list = []
for event in data:
    home_team = event["home_team"]
    away_team = event["away_team"]

    event_string = f"{home_team} vs {away_team}"
    event_list.append(event_string)
event_list.sort()

event_list_text.delete("1.0", "end")  # Clear existing text
event_list_text.insert("1.0", "\n".join(event_list))


team_list = ("Arizona Cardinals","Atlanta Falcons","Baltimore Ravens","Buffalo Bills","Carolina Panthers",
                              "Chicago Bears","Cincinnati Bengals","Cleveland Browns","Dallas Cowboys","Denver Broncos","Detroit Lions",
                              "Green Bay Packers","Houston Texans","Indianapolis Colts","Jacksonville Jaguars","Kansas City Chiefs",
                              "Las Vegas Raiders","Los Angeles Chargers","Los Angeles Rams","Miami Dolphins","Minnesota Vikings",
                              "New England Patriots","New Orleans Saints","New York Giants","New York Jets","Philadelphia Eagles",
                              "Pittsburgh Steelers","San Francisco 49ers","Seattle Seahawks","Tampa Bay Buccaneers","Tennessee Titans","Washington Commanders")

book_list = ("Barstool Sportsbook","BetMGM","BetOnline.ag","BetRivers","BetUS","Bovada","DraftKings","FanDuel","LowVig.ag","MyBookie.ag",
             "PointsBet (US)","SuperBook","Unibet","William Hill (US)")

value_t1inside = tk.StringVar(root)
value_t1inside.set("Select a Team")
value_t2inside = tk.StringVar(root)
value_t2inside.set("Select a Team")
value_binside = tk.StringVar(root)
value_binside.set("Select a Bookmaker")
# Create a dropdown menu
dropdown_team = tk.OptionMenu(root, value_t1inside, *team_list)
dropdown_team.pack()
dropdown_team = tk.OptionMenu(root, value_t2inside, *team_list)
dropdown_team.pack()
dropdown_book = tk.OptionMenu(root, value_binside, *book_list)
dropdown_book.pack()

def print_value():
    selected_team1 = value_t1inside.get()
    selected_team2 = value_t2inside.get()
    selected_bookmaker = value_binside.get()

    result_label.config(text="Selected Team 1: {}\nSelected Team 2: {}\nSelected Bookmaker: {}\n\nResults:".format(selected_team1, selected_team2, selected_bookmaker))
    
    results_text = ""
    # print("Selected Team 1:", selected_team1)
    # print("Selected Team 2:", selected_team2)
    # print("Selected Bookmaker:", selected_bookmaker,'\n')
    
    for event in data:
        if (event["home_team"] == selected_team1) and (event["away_team"] == selected_team2):
            for bookmaker in event["bookmakers"]:
                if bookmaker["title"] == selected_bookmaker:  
                    for market in bookmaker["markets"]:
                        if market["key"] == "spreads":
                            for outcome in market["outcomes"]:
                                outcome_name = outcome["name"]
                                outcome_point = outcome["point"]


                                results_text += "Outcome Name: {}\nOutcome Point: {}\n\n".format(outcome_name, outcome_point)
                                # print("Outcome Name:", outcome_name)
                                # print("Outcome Point:", outcome_point,"\n")
    results_label.config(text=results_text)                            
    
# Create a function to update the plot
def update_plot():
    selected_team1 = value_t1inside.get()
    selected_team2 = value_t2inside.get()
    selected_bookmaker = value_binside.get()

    ax.clear()  # Clear the previous plot

    x_labels = []
    team_data = {}  # Key: team name, Value: (x_values, y_values, color)

    # Iterate over the last 5 files and load JSON data for plots
    for idx, filename in enumerate(last_5_files):
        with open(os.path.join(directory, filename)) as jsonfile:
            file_data = json.load(jsonfile)
            
            # Extract the date and time part from the filename
            file_date_time_str = filename[-14:-5]  # Extract the last 14 characters
            x_labels.append(file_date_time_str)  # Convert to desired date and time format
            
            # Process the data as needed
            for event in file_data:
                if (event["home_team"] == selected_team1) and (event["away_team"] == selected_team2):
                    for bookmaker in event["bookmakers"]:
                        if bookmaker["title"] == selected_bookmaker:  
                            for market in bookmaker["markets"]:
                                if market["key"] == "spreads":
                                    for outcome in market["outcomes"]:
                                        team_name = outcome["name"]
                                        x_value = idx
                                        y_value = outcome["point"]
                                        color = 'blue' if team_name == selected_team1 else 'red'
                                        
                                        if team_name not in team_data:
                                            team_data[team_name] = ([], [], color)
                                        
                                        x_values, y_values, _ = team_data[team_name]
                                        x_values.append(x_value)
                                        y_values.append(y_value)

    # Plot connected dots with lines for each team
    for team_name, (x_values, y_values, color) in team_data.items():
        ax.plot(x_values, y_values, marker='o', color=color, label=team_name)
    
    ax.set_title(selected_bookmaker)
    ax.set_xlabel("Date")
    ax.set_ylabel("Point")
    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels, rotation=45, ha="right")  # Rotate x-labels for better visibility
    
    ax.legend()

    canvas.draw()  # Update the canvas to show the new plot

    # Adjust the layout
    plt.tight_layout()

# Create labels for displaying results
result_label = tk.Label(root, text="Selected Team 1:\nSelected Team 2:\nSelected Bookmaker:\n\nResults:")
result_label.pack()

results_label = tk.Label(root, text="")
results_label.pack()

def print_and_update():
    print_value()
    update_plot()

# Create a figure for the plot
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Submit button
submit_button = tk.Button(root, text='Submit and Update Plot', command=print_and_update)
submit_button.pack()

# Create a function to handle window close
def on_closing():
    plt.close()  # Close the matplotlib figure
    root.destroy()  # Close the tkinter window

# Bind the protocol event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main loop
root.mainloop()

