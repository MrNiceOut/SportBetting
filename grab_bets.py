import requests
from bs4 import BeautifulSoup
import csv
import numpy as np

# Login credentials
username = 'chrisjv2011@gmail.com'
password = 'Atcrocks1!'
csv_filename = 'scraped_data.csv'
scraped_data = []

login_url = 'https://www.vegasinsider.com/sign-in/'
data_url = 'https://www.vegasinsider.com/nfl/odds/las-vegas/'

# Create a session to maintain login state
session = requests.Session()

# Send a GET request to the login page
login_response = session.get(login_url)
login_soup = BeautifulSoup(login_response.content, 'html.parser')

# Find the input fields for username and password
username_input = login_soup.find('input', {'name': 'username'})
password_input = login_soup.find('input', {'name': 'password'})

# Prepare login data
login_data = {
    'username': username,
    'password': password,
}

# Send a POST request to login
post_response = session.post(login_url, data=login_data)
# Check if login was successful
if "200" in post_response.text:
    print("Login successful.")
    
    # Now you can access the protected page using the session
    data_response = session.get(data_url)
    
    if data_response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(data_response.content, 'html.parser')
        
        # Find the table element with the desired class name
        table = soup.find('table', class_='odds-table game-table')
        if table:
            # Iterate through rows in the table
            spread = table.find('tbody', class_='odds-table-spread--0')

            for row in spread.find_all('tr', class_=[None,'divided', 'footer']):
                # Extract the data
                game_team = row.find('td', class_='game-team')
                team_name = game_team.get_text(strip=True)

                game_odds_cell = row.find('td', class_='game-odds')
                if game_odds_cell:
                    disabled_span = game_odds_cell.find('span', class_='disabled')
                    
                    if disabled_span:
                        span_element = disabled_span.find('span', class_='data-value')
                        small_element = disabled_span.find('small', class_='data-odds')
                        
                        if span_element and small_element:
                            span_text = span_element.get_text(strip=True)
                            small_text = small_element.get_text(strip=True)
                    
                            row_data = {
                                'Team': team_name,
                                'Spread': span_text,
                                'vig': small_text
                            }
                            scraped_data.append(row_data)
        else:
            print("Table not found on the page.")
    else:
        print(f"Failed to retrieve the data page. Status code: {data_response.status_code}")
else:
    print("Login failed.")

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Team', 'Spread', 'vig']  # Add your desired field names here
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the scraped data rows
    for row_data in scraped_data:
        writer.writerow(row_data)

print(f"Scraped data has been saved to '{csv_filename}'.")



