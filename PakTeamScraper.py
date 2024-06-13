import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Function to extract player data from a single page
def extract_player_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # List to store player data
    player_data = []

    # Iterating over player profiles on the webpage
    for player in soup.find_all('div', class_='profile-repeat'):
        # Extracting basic player details
        name = player.find('div', class_='player-name').text.strip()
        country_element = player.find('td', class_='light-text-para', string='Country')
        country = country_element.find_next('td', class_='dark-text-val').text.strip() if country_element else None

        # Extracting Age and converting to Date of Birth
        age_element = player.find('td', class_='light-text-para', string='Age')
        age_text = age_element.find_next('td', class_='dark-text-val').text.strip() if age_element else None
        dob_match = re.search(r'(\d{1,2} \w+, \d{4})', age_text)
        dob = pd.to_datetime(dob_match.group(1), format='%d %b, %Y').strftime('%d/%m/%Y') if dob_match else None

        # Extracting Bat Style and removing " bat" at the end
        bat_style_element = player.find('td', class_='light-text-para', string='Bat Style')
        bat_style = bat_style_element.find_next('td', class_='dark-text-val').text.strip() if bat_style_element else None
        bat_style = bat_style.replace(' bat', '') if bat_style else None

        # Extracting Bowling Arm
        bowl_style_element = player.find('td', class_='light-text-para', string='Bowl Style')
        bowl_style = bowl_style_element.find_next('td', class_='dark-text-val').text.strip() if bowl_style_element else None

        # Using a try-except block to handle the case where re.search returns None
        try:
            bowling_arm = re.search(r'^(.*?)-arm', bowl_style).group(1).strip()
        except AttributeError:
            bowling_arm = '-'

        # Extracting Bowling Style based on specified conditions
        if re.search(r'offbreak|legbreak|orthodox', bowl_style, flags=re.IGNORECASE):
            bowling_style = 'Spin'
        elif not bowl_style or bowl_style == '-':
            bowling_style = '-'
        else:
            bowling_style = 'Pace'

        # Extracting Teams from the Team field that are part of PSL
        team_element = player.find('td', class_='light-text-para', string='Team')
        team_text = team_element.find_next('td', class_='dark-text-val').text.strip() if team_element else None

        psl_teams = ['Karachi Kings', 'Islamabad United', 'Lahore Qalandars', 'Peshawar Zalmi', 'Multan Sultans', 'Quetta Gladiators']
        teams = [team.strip() for team in team_text.split(',') if team.strip() in psl_teams]

        # Extracting ICC Rankings (not working properly atm)
        icc_ranking_element = player.find('td', class_='light-text-para', string='ICC Ranking')
        icc_ranking_text = icc_ranking_element.find_next('td', class_='dark-text-val').text.strip() if icc_ranking_element else None

        # Parsing ICC Rankings (getting only the values here, wasn't able to map on the dictionery properly :/ )
        ranking_values = [int(match.group(1)) for match in re.finditer(r'#?\s*(\d+)', icc_ranking_text)]

        player_data.append({
            'Name': name,
            'Country': country,
            'DateOfBirth': dob,
            'BatStyle': bat_style,
            'BowlingArm': bowling_arm,
            'BowlingStyle': bowling_style,
            'PSLTeams': ', '.join(teams),
            'ICCRankings': ranking_values[1:]
        })
    return player_data

# Function to scrape and transform data from multiple pages
def scrape_and_transform(base_url, pages):
    all_data = []
    for page_number in range(1, pages + 1):
        url = f"{base_url}page/{page_number}/"
        page_data = extract_player_data(url)
        print(f"Scraped {len(page_data)} players from {url}")
        all_data.extend(page_data)
    return all_data

# URL of the first page
base_url = "https://sportslumo.com/cricket/players/country/pakistan/"
pages = 4

# Scraping and transforming data from all pages
all_data = scrape_and_transform(base_url, pages)

# Creating a DataFrame
df = pd.DataFrame(all_data)

# Export to Excel
df.to_excel('check.xlsx', index=False)
