# Pakistan Cricket Players Data Scraper

This project scrapes data from the Pakistan Cricket Players section on the [SportsLumo website](https://sportslumo.com/cricket/players/country/pakistan/). The goal is to extract detailed information about each player, transform the data into a structured format, and export it to an Excel file.

## Table of Contents
- [Overview](#overview)
- [Data Extraction](#data-extraction)
- [Data Transformation](#data-transformation)
- [Export to Excel](#export-to-excel)
- [Example Output](#example-output)

## Overview
The project involves scraping data from the following link: [Pakistan Cricket Players](https://sportslumo.com/cricket/players/country/pakistan/) via Beautiful Soup Library. At the time of writing, there are four pages of player data. The tasks include:

1. Scraping data regarding each player of the Pakistan cricket team.
2. Transforming the scraped data into a set format with specific headers.
3. Exporting the transformed data into an Excel file.

## Data Extraction
The scraper will iterate through all available pages (currently 4) and extract relevant data for each player. The extracted data includes details such as player name, country, date of birth, bat style, bowling arm, bowling style, team, and ICC rankings.

## Data Transformation
The scraped data will be transformed according to the following mapping logic: (**For now I wasn't able to transform ICC Ranking properly so that field is still WIP**)

| Header        | Mapping Logic                                                | Example                                  |
|---------------|--------------------------------------------------------------|------------------------------------------|
| Name          | Take as is                                                   | Babar Azam                               |
| Country       | Take as is                                                   | Pakistan                                 |
| Date of Birth | Convert to DD/MM/YYYY format                                 | 15/10/1994                               |
| Bat Style     | Take as is (removing "bat" at the end of string)             | Right-Hand                               |
| Bowling Arm   | Left or Right based on the value in the Bowl Style field     | Right                                    |
| Bowling Style | Pace or Spin based on the value in the Bowl Style field      | Spin                                     |
| Team          | Only select those teams from the Team field which are part of PSL | Karachi Kings, Islamabad United         |
| ICC Ranking   | Capture all the rankings available from different cricket formats in a dictionary | {'T20 Bat': 1, 'ODI Bat': 1, 'Test Bat': 9, 'Test Bowl': 123, 'All Round': 83} |

## Export to Excel
After transforming the data, it will be exported to an Excel file named `pak_team.xlsx`.

## Demonstration
The final Excel sheet will look somewhat like this:

| Name       | Country  | DateOfBirth | BatStyle    | BowlingArm | BowlingStyle | PSLTeams                        | ICCRankings                                               |
|------------|----------|-------------|-------------|------------|--------------|---------------------------------|----------------------------------------------------------|
| Babar Azam | Pakistan | 15/10/1994  | Right-Hand  | Right      | Spin         | Karachi Kings, Islamabad United | {'T20 Bat': 1, 'ODI Bat': 1, 'Test Bat': 9, 'All Round': 83} |
| ...        | ...      | ...         | ...         | ...        | ...          | ...                             | ...                                                      |

![image](https://github.com/Eesha723/CricketPlayerStatsScraper/assets/81686688/fa2ab5cc-9f79-4620-b270-f3411892b075)

